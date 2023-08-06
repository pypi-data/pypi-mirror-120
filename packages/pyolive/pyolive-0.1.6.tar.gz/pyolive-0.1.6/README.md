PyOlive
=======

PyOlive is olive worker library.

Installing
----------

Install and update using `pip`_:

    $ pip install -U pyolive

A Simple Example
----------------

* app.py


    from pyolive import Olive

    app = Olive('dps.w10m')

    if __name__ == '__main__':
        import route
        route.add_resource(app)
        app.run()

* route.py


    from helloworld import HelloWorld

    def add_resource(app):
        app.add_resource(HelloWorld, 'ovw_hello')

* helloworld.py


    class HelloWorld:
        def __init__(self, **kwargs):
            self.channel = kwargs['channel']
            self.logger = kwargs['logger']
            self.context = kwargs['context']

        def main(self):
            self.logger.info("Start helloworld")
            self.channel.publish_notify(self.context, "Runnig step 1")
            self.context.set_filename("outfile.txt")
            return 0
