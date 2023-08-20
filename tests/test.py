import logging
import sys
from os import listdir
from os import path as os_path
from os import remove
from platform import machine, system
from subprocess import PIPE, STDOUT, Popen


def proc_exec(cmd, logger):
    """Execute command passed as an argument

    Args:
        cmd (list): bash command
        logger (object): logging object

    Raises:
        Exception: Process Failure
    """
    process = Popen(
        cmd, stdout=PIPE, stderr=STDOUT, universal_newlines=True, encoding="utf8"
    )
    out, err = process.communicate()
    if process.returncode != 0:
        logger.error(f"Process ReturnCode : {process.returncode}")
        logger.error(f"Process Error Output : \n{out}")
        raise Exception("Process Failed")


def set_ffmpeg_path():
    """Returns the path of ffmpeg executable

    Args:
        exec_os (Boolean): Windows -> True  Any-other-OS -> False

    Returns:
        str: ffmpeg execuatble path
    """
    if hasattr(sys, "getandroidapilevel"):
        bin = "ffmpeg_android_aarch64"
    else:
        bin = "ffmpeg_" + system().lower() + "_" + machine().lower()

    if system() == "Windows":
        bin = bin + ".exe"
    return os_path.join(os_path.dirname(__file__), "ffmpeg_bin", bin)


def test_ffmpeg_bin(logger):
    """A simple test suite to test
       ffmpeg binaries
    Args:
        logger (object): logging object
    """
    current_dir = os_path.dirname(__file__)
    logger.debug(f"CURRENT DIR : {current_dir}")
    test_files_path = os_path.join(current_dir, "test_files")
    logger.debug(f"TEST DIR : {test_files_path}")
    files_dict = {
        file.split(".")[-1]: os_path.join(test_files_path, file)
        for file in listdir(test_files_path)
    }
    ffmpeg = set_ffmpeg_path()
    output_path = {
        "webm": os_path.join(current_dir, "WEBM_FILE.webm"),
        "mp4": os_path.join(current_dir, "MP4_FILE.mp4"),
        "mp3": os_path.join(current_dir, "MP3_FILE.mp3"),
    }
    ffmpeg_threads = "4"
    webm_cmd = [
        ffmpeg,
        "-threads",
        ffmpeg_threads,
        "-y",
        "-loglevel",
        "verbose",
        "-i",
        "file:" + files_dict["webm"],
        "-i",
        "file:" + files_dict["weba"],
        "-c:v",
        "copy",
        "-c:a",
        "copy",
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "file:" + output_path["webm"],
        "-y",
    ]
    mp4_cmd = [
        ffmpeg,
        "-threads",
        ffmpeg_threads,
        "-y",
        "-loglevel",
        "verbose",
        "-i",
        "file:" + files_dict["mp4"],
        "-i",
        "file:" + files_dict["m4a"],
        "-i",
        "file:" + files_dict["jpg"],
        "-c:v",
        "copy",
        "-c:a",
        "copy",
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "-map",
        "2",
        "-disposition:2",
        "attached_pic",
        "file:" + output_path["mp4"],
        "-y",
    ]
    mp3_cmd = [
        ffmpeg,
        "-threads",
        ffmpeg_threads,
        "-y",
        "-loglevel",
        "verbose",
        "-i",
        "file:" + files_dict["m4a"],
        "-acodec",
        "libmp3lame",
        "-b:a",
        "192k",
        "file:" + output_path["mp3"],
        "-y",
    ]

    for cmd, ext in zip((webm_cmd, mp4_cmd, mp3_cmd), ("webm", "mp4", "mp3")):
        # check if ffmpeg is working as intended
        proc_exec(cmd, logger)
        cmd = [
            ffmpeg,
            "-v",
            "error",
            "-i",
            "file:" + output_path[ext],
            "-c",
            "copy",
            "-f",
            "null",
            "-",
        ]
        # check the file integrity of the generated output file
        proc_exec(cmd, logger)
        logger.debug(f"{ext} Test Passed!!")
    print("All test passed!!")
    # delete newly generated files
    for path in output_path.values():
        try:
            remove(path)
            logger.debug(f"Removed file : {path}")
        except FileNotFoundError:
            pass


def get_logger():
    # define log handler
    logger = logging.getLogger("ffmpeg-tester")
    handler = logging.FileHandler(
        filename=os_path.join(os_path.dirname(__file__), "ffmpeg_test.log"), mode="w"
    )
    logger.setLevel(level=logging.DEBUG)
    logger.addHandler(handler)
    # define formatter
    log_formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(message)s", datefmt="%d-%b-%y %H:%M:%S"
    )
    handler.setFormatter(log_formatter)
    return logger


def main():
    logger = get_logger()
    test_ffmpeg_bin(logger)


if __name__ == "__main__":
    main()
