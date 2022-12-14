FROM python:3.5

RUN pip install --upgrade pip && \
    pip install nltk && \
    pip install flask flask_json

RUN mkdir -p falsefriends
COPY ./ /falsefriends
WORKDIR /falsefriends/
RUN python --version && \
    pip install Cython && \
    pip install -r requirements.txt


ENV LANG="C.UTF-8" \
    LC_ALL="C.UTF-8"

RUN wget https://github.com/pln-fing-udelar/false-friends/archive/refs/heads/master.zip \
	&& unzip master.zip \
    && mv false-friends-master falsefriendsp \
    && touch falsefriendsp/__init__.py

RUN python -m nltk.downloader wordnet \
    && python -m nltk.downloader omw


##download models
RUN wget http://cs.famaf.unc.edu.ar/~ccardellino/SBWCE/SBW-vectors-300-min5.txt.bz2 \
    && bzip2 -d SBW-vectors-300-min5.txt.bz2

RUN wget http://143.107.183.175:22980/download.php?file=embeddings/word2vec/skip_s300.zip \
    && unzip download.php?file=embeddings%2Fword2vec%2Fskip_s300.zip

RUN mkdir falsefriendsp/resources/big \
    && mv SBW-vectors-300-min5.txt falsefriendsp/resources/big/es.txt \
    && mv skip_s300.txt falsefriendsp/resources/big/pt.txt

EXPOSE 8866

#COPY ./ ./
CMD ["python", "serve.py"]
