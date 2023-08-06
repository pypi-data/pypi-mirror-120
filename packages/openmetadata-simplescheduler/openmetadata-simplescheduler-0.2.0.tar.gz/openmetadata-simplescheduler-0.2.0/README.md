# OpenMetadata Simple Scheduler

We are going to build a library
based on simple scheduler for only cron-related ingestion purpose. 

# Scheduler

``openmetadata-simplescheduler`` is a flexible python library for building your own cron-like system to schedule jobs, which is to run a tornado process to serve REST APIs and a web ui.



## Try it NOW

From source code:

    git clone https://github.com/open-metadata/simplescheduler.git
    cd simplescheduler
    make simple

Open your browser and go to [localhost:7777](http://localhost:7777). 

## How to build Your own cron-replacement

### Install simplescheduler
Using pip (from GitHub repo)

    #
    # Put this in requirements.txt, then run
    #    pip install -r requirements.txt
    #

    # If you want the latest build
    git+https://github.com/open-metadata/simplescheduler.git#egg=simplescheduler

    
    pip install -e git+https://github.com/open-metadata/simplescheduler.git#egg=simplescheduler

### Three things

You have to implement three things for your scheduler, i.e., ``Settings``, ``Server``, and ``Jobs``.

**Settings**

In your implementation, you need to provide a settings file to override default settings (e.g., [settings in simple_scheduler](https://github.com/Open-Metadata/simplescheduler/blob/master/simple_scheduler/settings.py)). You need to specify the python import path in the environment variable ``SIMPLESCHEDULER_SETTINGS_MODULE`` before running the server.

All available settings can be found in [default_settings.py](https://github.com/Open-Metadata/simplescheduler/blob/master/simplescheduler/default_settings.py) file.

**Server**

You need to have a server file to import and run ``sdscheduler.server.server.SchedulerServer``.

**Jobs**

Each job should be a standalone class that is a subclass of ``sdscheduler.job.JobBase`` and put the main logic of the job in ``run()`` function.

After you set up ``Settings``, ``Server`` and ``Jobs``, you can run the whole thing like this:

    SIMPLESCHEDULER_SETTINGS_MODULE=simple_scheduler.settings \
    PYTHONPATH=.:$(PYTHONPATH) \
		    python simple_scheduler/scheduler.py
		  
**Install dependencies**

    # Each time we introduce a new dependency in setup.py, you have to run this
    make install

**Run unit tests**

    make test
    
**Clean everything and start from scratch**
    
    make clean




    
