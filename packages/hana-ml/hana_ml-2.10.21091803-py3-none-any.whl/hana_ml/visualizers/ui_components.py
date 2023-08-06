# pylint: disable=too-many-arguments
# pylint: disable=too-few-public-methods
# pylint: disable=line-too-long
# pylint: disable=too-many-locals
# pylint: disable=missing-docstring
# pylint: disable=invalid-name
# pylint: disable=unused-variable
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements
# pylint: disable=trailing-newlines
import html
import time
from threading import Lock
# https://github.com/ipython/ipython/blob/master/IPython/display.py
from IPython.core.display import HTML, display
from htmlmin.main import minify
from hana_ml.visualizers.model_report import TemplateUtil


class IdGenerator(object):
    def __init__(self):
        self.base_id = 0
        self.lock = Lock()
        self.current_time = (str(int(time.time() * 1000)))[::-1]

    def id(self):
        self.lock.acquire()
        new_id = self.base_id + 1
        self.base_id = new_id
        self.lock.release()
        return str(new_id) + self.current_time


idGenerator = IdGenerator()

build_html_exception_msg = 'To generate an HTML page, you must call the build method firstly.'
passed_parameter_value_exception_msg = "The value of parameter '{}' is null. Please check your passed parameter."


class HTMLUtils(object):
    @staticmethod
    def minify(html_str):
        return minify(html_str,
                      remove_all_empty_space=True,
                      remove_comments=True,
                      remove_optional_attribute_quotes=False)


class HTMLFrameUtils(object):
    @staticmethod
    def display(frame_html):
        display(HTML(frame_html))

    @staticmethod
    def check_frame_height(frame_height):
        if 300 <= int(frame_height) <= 800:
            pass
        else:
            raise ValueError("The parameter 'frame_height' value is invalid! The effective range is [300,800].")

    @staticmethod
    def build_frame_src(html_str):
        frame_src = html.escape(html_str)
        return frame_src

    @staticmethod
    def build_frame_html_with_id(frame_id, frame_src, frame_height):
        frame_html = """
            <iframe
                id="{iframe_id}"
                width="{width}"
                height="{height}"
                srcdoc="{src}"
                style="border:1px solid #ccc"
                allowfullscreen="true"
                webkitallowfullscreen="true"
                mozallowfullscreen="true"
                oallowfullscreen="true"
                msallowfullscreen="true"
            >
            </iframe>
        """.format(
            iframe_id=frame_id,
            width='99.80%',
            height=frame_height,
            src=frame_src,
        )

        return frame_html

    @staticmethod
    def build_frame_html(frame_src, frame_height):
        frame_html = """
            <iframe
                width="{width}"
                height="{height}"
                srcdoc="{src}"
                style="border:1px solid #ccc"
                allowfullscreen="true"
                webkitallowfullscreen="true"
                mozallowfullscreen="true"
                oallowfullscreen="true"
                msallowfullscreen="true"
            >
            </iframe>
        """.format(
            width='99.80%',
            height=frame_height,
            src=frame_src,
        )

        return frame_html


class Fullscreen(object):
    __TEMPLATE = TemplateUtil.get_template('fullscreen.html')

    def __init__(self, target_iframe_type):
        if target_iframe_type is None:
            raise Exception(passed_parameter_value_exception_msg.format('target_iframe_type'))

        self.html = None
        self.frame_src = None
        self.frame_html = None

        self.target_frame_id = idGenerator.id()
        self.target_frame_type = target_iframe_type

        # build
        self.html = Fullscreen.__TEMPLATE.render(iframe_id=self.target_frame_id, iframe_type=self.target_frame_type)
        self.html = HTMLUtils.minify(self.html)
        self.frame_src = HTMLFrameUtils.build_frame_src(self.html)
        self.frame_html = HTMLFrameUtils.build_frame_html(self.frame_src, '80px')

    def generate_notebook_iframe(self):
        HTMLFrameUtils.display(self.frame_html)


class JSONViewer(object):
    __TEMPLATE = TemplateUtil.get_template('json.html')

    def __init__(self, data):
        if data is None:
            raise Exception(passed_parameter_value_exception_msg.format('data'))

        self.html = None
        self.frame_src = None
        self.frame_html = None

        self.data = data

        self.fullscreen = Fullscreen('json')
        self.frame_id = self.fullscreen.target_frame_id

        # build
        self.html = JSONViewer.__TEMPLATE.render(data_json_dict=self.data)
        self.html = HTMLUtils.minify(self.html)
        self.frame_src = HTMLFrameUtils.build_frame_src(self.html)

    def generate_html(self, filename):
        TemplateUtil.generate_html_file('{}_json.html'.format(filename), self.html)

    def generate_notebook_iframe(self, iframe_height='300'):
        HTMLFrameUtils.check_frame_height(iframe_height)
        self.frame_html = HTMLFrameUtils.build_frame_html_with_id(self.frame_id, self.frame_src, iframe_height)

        self.fullscreen.generate_notebook_iframe()
        HTMLFrameUtils.display(self.frame_html)


class XMLViewer(object):
    __TEMPLATE = TemplateUtil.get_template('xml.html')

    def __init__(self, data):
        if data is None:
            raise Exception(passed_parameter_value_exception_msg.format('data'))

        self.html = None
        self.frame_src = None
        self.frame_html = None

        self.data = data

        self.fullscreen = Fullscreen('xml')
        self.frame_id = self.fullscreen.target_frame_id

        # build
        self.html = XMLViewer.__TEMPLATE.render(data_xml_dict=self.data)
        self.html = HTMLUtils.minify(self.html)
        self.frame_src = HTMLFrameUtils.build_frame_src(self.html)

    def generate_html(self, filename):
        TemplateUtil.generate_html_file('{}_xml.html'.format(filename), self.html)

    def generate_notebook_iframe(self, iframe_height='300'):
        HTMLFrameUtils.check_frame_height(iframe_height)
        self.frame_html = HTMLFrameUtils.build_frame_html_with_id(self.frame_id, self.frame_src, iframe_height)

        self.fullscreen.generate_notebook_iframe()
        HTMLFrameUtils.display(self.frame_html)
