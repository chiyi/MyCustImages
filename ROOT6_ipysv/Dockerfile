FROM rootproject/root:6.26.04-ubuntu22.04

MAINTAINER kaiyi

RUN apt update -y
RUN apt install -y python3-numpy python3-scipy python3-notebook python3-pandas
RUN apt install -y ipython3 jupyter
RUN apt install -y vim
RUN python3.10 -m pip install ipykernel jupyter_server notebook==6.5.6
RUN pip3 install metakernel zmq
RUN pip3 install -U scikit-learn
RUN apt install -y net-tools
RUN apt install -y graphviz
RUN apt update -y && apt install -y r-base


RUN mkdir /root/IPyNB
ADD jupyter_notebook_config.template /root/jupyter_notebook_config.py
ADD Demo.ipynb /root/IPyNB/Demo.ipynb
ADD Demo2.ipynb /root/IPyNB/Demo2.ipynb
ADD Demo_GaussianErrorBar.ipynb /root/IPyNB/Demo_GaussianErrorBar.ipynb
ADD Demo_BinomialErrorBar.ipynb /root/IPyNB/Demo_BinomialErrorBar.ipynb
ADD Demo_BinomialErrorBar_catbins.ipynb /root/IPyNB/Demo_BinomialErrorBar_catbins.ipynb
ADD Demo_BinomialErrorBar_dynbins.ipynb /root/IPyNB/Demo_BinomialErrorBar_dynbins.ipynb
ADD PyNBPlotStyles /root/IPyNB/PyNBPlotStyles
ADD demo_data /root/IPyNB/demo_data
ADD jsroot.zip /root/jsroot

ADD Test_BiasCheck.ipynb /root/IPyNB/Test_BiasCheck.ipynb
ADD cust_func.C /root/IPyNB/cust_func.C

WORKDIR /root/IPyNB

ADD run_notebook.sh /root/run_notebook.sh
RUN chmod +x /root/run_notebook.sh

CMD ["/root/run_notebook.sh"]
