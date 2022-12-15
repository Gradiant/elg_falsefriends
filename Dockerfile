FROM python:3.5 AS base

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir flask flask_json

RUN mkdir -p falsefriends
COPY requirements.txt /falsefriends/
WORKDIR /falsefriends/
RUN python --version && \
    pip install --no-cache-dir Cython==0.29.32 && \
    pip install --no-cache-dir -r requirements.txt


ENV LANG="C.UTF-8" \
    LC_ALL="C.UTF-8"

RUN wget https://github.com/pln-fing-udelar/false-friends/archive/refs/heads/master.zip \
	&& unzip master.zip \
        && rm master.zip \
    && mv false-friends-master falsefriendsp \
    && touch falsefriendsp/__init__.py

RUN python -m nltk.downloader wordnet \
    && python -m nltk.downloader omw

## fork build here - create a temporary stage to pre-process the models
FROM base as modelbuilder

##download models and store in build cache
RUN mkdir model-data \
    && wget --progress=dot:giga -O model-data/es.txt.bz2 http://cs.famaf.unc.edu.ar/~ccardellino/SBWCE/SBW-vectors-300-min5.txt.bz2

RUN wget --progress=dot:giga -O model-data/skip_s300.zip http://143.107.183.175:22980/download.php?file=embeddings/word2vec/skip_s300.zip \
    && cd model-data && unzip skip_s300.zip skip_s300.txt && rm skip_s300.zip

# pre-compile model files into fast-loading KeyedVectors format
COPY buildscripts/w2v_to_kv.py buildscripts/

RUN mkdir model-files && python buildscripts/w2v_to_kv.py model-data/es.txt.bz2 model-files/es.kv
RUN python buildscripts/w2v_to_kv.py model-data/skip_s300.txt model-files/pt.kv

# pre-compile linear transform and training pairs and save in npz format
COPY buildscripts/build_linear_trans.py buildscripts/
RUN PYTHONPATH=/falsefriends python buildscripts/build_linear_trans.py model-files/es.kv model-files/pt.kv model-files/trans_es_300_pt_300.npz \
      model-files/training_pairs.npz

## go back to the fork point and copy just the final compiled files into the runtime image
FROM base AS runtime

EXPOSE 8866

COPY --from=modelbuilder /falsefriends/model-files/ ./falsefriendsp/resources/big/

COPY serve.py ./
CMD ["python", "serve.py"]
