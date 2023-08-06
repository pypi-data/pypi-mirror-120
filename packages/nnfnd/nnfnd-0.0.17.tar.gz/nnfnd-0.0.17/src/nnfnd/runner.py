import os
import json
import subprocess
import zipfile
import logging
from typing import Any
import requests
import time
import csv
import tornado.ioloop
import tornado.web
import tornado.httpserver
import shutil


class Runner:
    _app = None
    _script_path = None
    _port = None
    _inference_model = None

    def __init__(self, script_path, flags, port=80, inference_model=None):
        app = make_app()
        app.settings.update({'script_path': script_path, 'flags': flags})

        if inference_model is not None:
            raise "'inference_model' not supported now"

        self._port = port
        self._inference_model = inference_model
        self._app = app

    def run(self):
        logging.info(f"Init app: {self._port}")

        server = tornado.httpserver.HTTPServer(self._app, max_buffer_size=10485760000)  # 10G
        server.listen(self._port)
        tornado.ioloop.IOLoop.current().start()


class InferHandler(tornado.web.RequestHandler):
    parsed_body = None
    uploads_dir = "uploads/"

    def write_error(self, status_code: int, **kwargs: Any) -> None:
        logging.info(f"[write_error]: {status_code} | {kwargs}")

        message = 'internal server error'
        if 'message' in kwargs:
            message = kwargs['message']

        self.finish(json.dumps({'success': False, 'message': message}))

    # def prepare(self):
    #     data = json_decode(self.request.body)
    #     if 'input' not in data or data['input'] == "":
    #         self.finish({'success': False, 'message': 'input field required'})
    #     if 'output' not in data or data['output'] == "":
    #         self.finish({'success': False, 'message': 'output field required'})
    #     self.parsed_body = data

    @staticmethod
    def parse_model_result(results_path):
        res = dict()

        # INFO: file format: filename, label, confidence, X, Y, W, H
        with open(results_path) as csvfile:
            rows = csv.reader(csvfile)
            skipped_first_line = False
            for row in rows:
                print("###", row)
                logging.info(f"row: {row}")

                filename = row[0]

                if not skipped_first_line:
                    skipped_first_line = True
                    continue

                if filename not in res:
                    res[filename] = []

                item = {
                    'label': row[1],
                    'confidence': row[2]
                }

                res[filename].append(item)

        return res

    def run_model(self, input_path, output_path):
        script_path = self.settings.get('script_path')
        args = [
            'python', script_path,
            '--input', input_path,
            '--output', output_path
        ]

        flags = self.settings.get('flags')
        if flags is not None and type(flags) == dict:
            for key in flags.keys():
                args.extend([key, flags[key]])

        script_cmd = ' '.join(args)

        print('run script: ', script_cmd)
        logging.info(f'run script: {script_cmd}')

        # INFO: after update to python3.7 use 'capture_output=True' instead
        #   'stdout=subprocess.PIPE, stderr=subprocess.PIPE'
        result = subprocess.run(script_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        print("script out: ", result.stdout)
        logging.info(f'script out: {result.stdout.decode("utf-8")}')

        if result.returncode != 0:
            self.write_error(500, message=f'model exit with {result.returncode} code')
            return 'error'

        results_path = os.path.join(output_path, 'result.csv')
        if not os.path.exists(results_path):
            return None
        return self.parse_model_result(results_path)

    def async_execution(self, input_path, output_path, url_post_result):
        body = self.run_model(input_path, output_path)
        requests.post(url_post_result, json=body)

    def post(self):
        self.set_header('Content-Type', 'application/json')
        archive = self.request.files.get('archive')

        if archive is None:
            self.set_status(400)
            self.write(json.dumps({'message': 'archive required'}))
            return

        url_post_result = self.get_body_argument('urlPostResult', '')
        async_mode = url_post_result != ''

        archive_filename = archive[0]['filename']

        logging.info("archive_filename: ", archive_filename)

        ts = int(time.time())

        upload_dir_with_ts = os.path.join(self.uploads_dir, str(ts))

        save_path = os.path.join(upload_dir_with_ts, archive_filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        output_file = open(save_path, 'wb')
        output_file.write(archive[0]['body'])

        with zipfile.ZipFile(save_path, 'r') as zip_ref:
            zip_ref.extractall(upload_dir_with_ts)

        print('async_mode: ', async_mode, url_post_result)

        if async_mode:
            self.finish({'success': True})
            self.async_execution(
                input_path=upload_dir_with_ts,
                output_path=upload_dir_with_ts,
                url_post_result=url_post_result)
            return

        body = self.run_model(input_path=upload_dir_with_ts, output_path=upload_dir_with_ts)
        if body is None:
            self.set_status(204)
            self.finish()
            return

        if body == 'error':
            return

        try:
            shutil.rmtree(upload_dir_with_ts)
        except OSError as e:
            logging.error(f"remove dir with screenshots: {upload_dir_with_ts}: {e.strerror}")

        self.finish(json.dumps(body))


def make_app():
    return tornado.web.Application([
        (r"/api/v1/infer", InferHandler),
    ])
