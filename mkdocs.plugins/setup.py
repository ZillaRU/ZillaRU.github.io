from setuptools import setup, find_packages

setup(
    name='custom_footer_plugin',  # 替换为您的插件名称
    version='1.0',  # 替换为您的插件版本号
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'custom_footer_plugin = custom_footer_plugin:CustomFooterPlugin'
        ]
    }
)
