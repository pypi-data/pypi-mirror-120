import asyncio
import binascii
import hashlib
import os

import aiofiles
import aiohttp
import xlrd3

from . import _getHeaderByDefault, makeFolder
from .log import warning

_maxAsyncFileNum = 5000
_currentAsyncFileNum = 0
_waitAsyncFileTime = 0.5


def setAsyncFileMaxNum(value):
    global _maxAsyncFileNum
    _maxAsyncFileNum = value


async def asyncAwait(*taskList):
    resultList = []
    for task in taskList:
        resultList.append(await task)
    return resultList


async def asyncWriteFile(file, data, encoding='utf8', newline='\n'):
    makeFolder(os.path.dirname(file))
    global _currentAsyncFileNum
    while _currentAsyncFileNum > _maxAsyncFileNum:
        await asyncio.sleep(_waitAsyncFileTime)
    _currentAsyncFileNum += 1
    async with aiofiles.open(file, 'w', encoding=encoding, newline=newline) as f:
        await f.write(data)
        await f.flush()
        await f.close()
    _currentAsyncFileNum -= 1


async def asyncWriteBinFile(file, data):
    makeFolder(os.path.dirname(file))
    global _currentAsyncFileNum
    while _currentAsyncFileNum > _maxAsyncFileNum:
        await asyncio.sleep(_waitAsyncFileTime)
    _currentAsyncFileNum += 1
    async with aiofiles.open(file, 'wb') as f:
        await f.write(data)
        await f.flush()
        await f.close()
    _currentAsyncFileNum -= 1


async def asyncReadFile(file, encoding='utf8', newline='\n'):
    global _currentAsyncFileNum
    while _currentAsyncFileNum > _maxAsyncFileNum:
        await asyncio.sleep(_waitAsyncFileTime)
    _currentAsyncFileNum += 1
    async with aiofiles.open(file, 'r', encoding=encoding, newline=newline) as f:
        data = await f.read()
        await f.close()
    _currentAsyncFileNum -= 1
    return data


async def asyncReadBinFile(file):
    global _currentAsyncFileNum
    while _currentAsyncFileNum > _maxAsyncFileNum:
        await asyncio.sleep(_waitAsyncFileTime)
    _currentAsyncFileNum += 1
    async with aiofiles.open(file, 'rb') as f:
        data = await f.read()
        await f.close()
    _currentAsyncFileNum -= 1
    return data


async def asyncOpenXlsx(file):
    data = await asyncReadBinFile(file)
    return xlrd3.open_workbook(file_contents=data, formatting_info=True)
    # 只提供了异步打开xlsx的方法，没有提供异步写入xlsx的方法，因为xlwt不支持


async def asyncGetFileMD5(file):
    data = await asyncReadBinFile(file)
    return hashlib.md5(data).hexdigest()


async def asyncGetFileCRC32(file):
    data = await asyncReadBinFile(file)
    return binascii.crc32(data)


async def asyncGetFileCRCHex(file):
    return hex(await asyncGetFileCRC32(file))[2:].zfill(8)


async def asyncExecute(*parList):
    # 注意：针对windows，版本是3.8以下需要使用asyncio.subprocess，在执行main之前就要执行
    # 注意：在3.7如果调用对aiohttp有异常报错
    # asyncio.set_event_loop_policy(
    #    asyncio.WindowsProactorEventLoopPolicy()
    # )

    proc = await asyncio.create_subprocess_shell(
        ' '.join(parList),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    return proc.returncode, stdout, stderr


_maxAsyncHttpNum = 3
_currentAsyncHttpNum = 0
_waitAsyncHttpTime = 0.1


def setAsyncHttpMaxNum(value):
    global _maxAsyncHttpNum
    _maxAsyncHttpNum = value


async def asyncHttpGet(url, headers=None, timeout=30, retry=3):
    initAioHttp()
    global _currentAsyncHttpNum
    headers = _getHeaderByDefault(headers)
    result = None
    response = None
    currentTry = 0
    while _currentAsyncHttpNum >= _maxAsyncHttpNum:
        await asyncio.sleep(_waitAsyncHttpTime)
    _currentAsyncHttpNum += 1
    while currentTry < retry:
        currentTry += 1
        try:
            response = None
            async with aiohttp.ClientSession() as session:
                response = await session.get(
                    url,
                    headers=headers,
                    timeout=timeout,
                )
                result = await response.read()
                response.close()
                # await session.close()
                if not result:
                    continue
                break
        except Exception:
            if response:
                response.close()
            warning(f'async http get exception url={url} times={currentTry}')
    _currentAsyncHttpNum -= 1
    return result, response


async def asyncHttpPost(url, data=None, headers=None, timeout=30, retry=3):
    initAioHttp()
    global _currentAsyncHttpNum
    headers = _getHeaderByDefault(headers)
    result = None
    response = None
    currentTry = 0
    while _currentAsyncHttpNum >= _maxAsyncHttpNum:
        await asyncio.sleep(_waitAsyncHttpTime)
    _currentAsyncHttpNum += 1
    while currentTry < retry:
        currentTry += 1
        try:
            response = None
            async with aiohttp.ClientSession() as session:
                response = await session.post(
                    url,
                    data=data,
                    headers=headers,
                    timeout=timeout,
                )
                result = await response.read()
                response.close()
                # await session.close()
                if not result:
                    continue
                break
        except Exception:
            if response:
                response.close()
            warning(f'async http get exception url={url} times={currentTry}')
    _currentAsyncHttpNum -= 1
    return result, response


async def asyncDownload(url, file):
    result, _response = await asyncHttpGet(url)
    await asyncWriteBinFile(file, result)


isInitAioHttp = True


def initAioHttp():

    global isInitAioHttp
    if isInitAioHttp:
        isInitAioHttp = False
    else:
        return

    from asyncio.proactor_events import _ProactorBasePipeTransport
    from functools import wraps

    # 尝试优化报错：RuntimeError: Event loop is closed

    def silence_event_loop_closed(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except RuntimeError as e:
                if str(e) != 'Event loop is closed':
                    raise
        return wrapper

    _ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)
