from Gat.util.methodtracer import traceFrameMessage


class MethodInvoker(object):
    """
    动态调用方法
    """
    @staticmethod
    def get_instance(moudelname,classname,packagelist):
        moudel=__import__(moudelname,fromlist=packagelist)
        klass = getattr(moudel,classname)
        instance = klass()
        print(instance)
        traceFrameMessage()
        return instance

    @staticmethod
    def get_method(instance,methodname):
        method=getattr(instance,methodname)
        return method

