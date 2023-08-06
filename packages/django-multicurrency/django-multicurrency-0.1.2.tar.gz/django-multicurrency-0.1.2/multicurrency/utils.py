import importlib

def import_class(class_path:str) -> object:
    """
        Function return class by string path:
            class_path: module1.sub_module.file.MyClass
        return MyClass
    """
    # get split module path and class name from class path
    module_path, class_name = \
        class_path[:class_path.rfind('.')], class_path[class_path.rfind('.')+1:]

    # import module and return class from module
    module = importlib.import_module(module_path)
    return getattr(module, class_name)
    