1, Purpose: A robust NLP pipleline tools based on the open source spaCy platform, but to be customerized for Weibo data and applications

2, Installation:
   a. Create an virtual environment, i.e.
      python3 -m venv ./'wbnlu-venv'
	  source wbnlu-venv/bin/activate

   b. Compile && locally install spaCy-weibo:
      cd spaCy-weibo
      pip install wheel (if errors messages: "Failed building wheel for ...")
      pip install cython
      pip install -r requirements.txt
      python setup.py build_ext --inplace
      pip install -e . (or pip install . for deployment)

   c. Install chinese model:
      cd ../
      scp -P 33 root@10.87.52.131:/data0/public/wb-nlp-tool/model-files/zh/zh_core_web_lg-2.3.1.tar.gz model-files/zh/
      pip install model-files/zh/zh_core_web_lg-2.3.1.tar.gz
      python -m spacy link zh_core_web_lg zh_lg_model

   d. Copy WB tag pattern files (optional, except for weibo content tagging):
       scp -P 33 root@10.87.52.131:/data0/public/wb-nlp-tool/nlu-weibo/wbnlu/resources/features/wbtag/* nlu-weibo/wbnlu/resources/features/wbtag/

   e. Install public API
      cd ./nlu-weibo
      pip install -e . (or pip install . for deployment)
      

3. Test:
   ipython
   import wbnlu
   print(wbnlu.nlp("我喜欢美妆里面的碧唇果酸面膜", enable=['segmenter']))

4. To start http service:
   cd $wb-nlp-tool/nlu-weibo/http
   python service_host.py

5. To open Jupyter Notebook from wbnlu2.0/ run:
   jupyter notebook
