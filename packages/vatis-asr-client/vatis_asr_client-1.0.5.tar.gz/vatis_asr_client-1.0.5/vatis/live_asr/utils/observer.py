from typing import Optional

from vatis.live_asr.stream.observer import LiveStreamObserver, ResponseMetadata
from vatis.asr_commons.domain.transcriber import TimestampedTranscriptionPacket
from vatis.asr_commons.live.headers import FINAL_FRAME_HEADER, FRAME_START_TIME_HEADER, FRAME_END_TIME_HEADER

import sys
from io import IOBase


class LoggingLiveStreamObserver(LiveStreamObserver):
    """
    Conventional stream observer for logging events
    """
    from logging import Logger

    def __init__(self, logger: Logger = None):
        super().__init__()
        self._logger = logger

    def on_connect(self):
        message = 'Stream connected'

        if self._logger is not None:
            self._logger.info(message)
        else:
            print(message)

    def on_disconnect(self):
        message = 'Stream disconnected'

        if self._logger is not None:
            self._logger.info(message)
        else:
            print(message)

    def on_response(self, packet: TimestampedTranscriptionPacket, metadata: ResponseMetadata):
        final_frame = 'FINAL' if packet.get_header(FINAL_FRAME_HEADER, default=False) else 'PARTIAL'
        message = f'{metadata.processing_time:.2f}s {final_frame:7s} : {packet.transcript}'

        if self._logger is not None:
            self._logger.info(message)
        else:
            print(message)

    def on_close(self):
        message = 'Stream closed'

        if self._logger is not None:
            self._logger.info(message)
        else:
            print(message)

    def on_transcription_completed(self):
        message = 'Transcription completed'

        if self._logger is not None:
            self._logger.info(message)
        else:
            print(message)


class FormattedLiveStreamObserver(LiveStreamObserver):
    """
    Utility class for formatting and redirecting the responses to an output stream
    """
    def __init__(self, out: Optional[IOBase] = None):
        if out is None:
            out = sys.stdout

        self._out = out

    def on_response(self, packet: TimestampedTranscriptionPacket, metadata: ResponseMetadata):
        if packet.get_header(FINAL_FRAME_HEADER, default=False):
            self._out.write('FINAL  : {0:.2f} -> {1:.2f}: {2}\n'.format(
                packet.get_header(FRAME_START_TIME_HEADER),
                packet.get_header(FRAME_END_TIME_HEADER),
                packet.transcript
            ))

        else:
            self._out.write('PARTIAL: {0:.2f} -> {1:.2f}: {2}\r'.format(
                packet.get_header(FRAME_START_TIME_HEADER),
                packet.get_header(FRAME_END_TIME_HEADER),
                packet.transcript
            ))
            self._out.flush()
