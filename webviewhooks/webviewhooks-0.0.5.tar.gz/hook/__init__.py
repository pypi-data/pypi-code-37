from hook import _hook

_web_view_hook_instance = None


def hook(package_name, device_id, callback, adb_name='adb'):
    global _web_view_hook_instance
    _web_view_hook_instance = _hook.WebViewHook(package_name, device_id, callback, adb_name)
    _web_view_hook_instance.hook()


def clear():
    global _web_view_hook_instance
    if _web_view_hook_instance is None:
        raise RuntimeError('sorry you should call hook first')
    _web_view_hook_instance.clear()
