Run the demo application
========================

Type these commands in the terminal:

.. code-block:: bash

    $ git clone https://github.com/lorist/pexservicepolicy.git
    $ cd pexservicepolicy
    $ virtualenv -p python3 venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ python app.py

Now go to http://localhost:5000.
If you want to populate the DB with some test data, uncomment:

.. code-block:: python

    # db.drop_all()
    # db.create_all()
    # for i in range(100):
    #     v = Vmrs()
    #     v.local_alias = "vmr" + str(i)
    #     v.name = "VMR " + str(i)
    #     db.session.add(v)
    # db.session.commit()

Be sure to comment again after the DB is created or it will overwrite every time :)

To Test with Pexip. I would use ngrok to present a public URL that you can point the conference nodes to.

Create a policy profile in Pexip and point it to the ngrok URL for Service Configuration. The app will then receive policy requests.

Run in docker
========================

Build from source:

.. code-block:: bash

    docker build -t pexservicepolicy .
    docker run -d -p 5000:5000 pexservicepolicy

    
Thanks to https://bootstrap-flask.readthedocs.io
