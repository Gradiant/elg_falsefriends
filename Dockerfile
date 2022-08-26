FROM python3.5:latest

RUN apt-get update -y \
	&& apt-get install -y python3-pip python3-dev \
    && apt-get install -y wget \
	&& apt-get install -y bzip2 \
    && apt-get install -y unzip \
	&& rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install flask flask_json
RUN pip install -r requiremements.txt


ENV LANG="C.UTF-8" \
    LC_ALL="C.UTF-8"

RUN wget https://github.com/pln-fing-udelar/false-friends/archive/refs/heads/master.zip \
	&& unzip false-friends-master.zip \
    && mv false-friends falsefriendsp \
    && touch falsefriendsp/__init__.py \

RUN python -m nltk.downloader wordnet \
    && python -m nltk.downloader omw

##download repository
RUN wget https://github.com/pln-fing-udelar/false-friends/archive/refs/heads/master.zip \
	&& unzip false-friends-master.zip \

##download models
RUN wget http://cs.famaf.unc.edu.ar/~ccardellino/SBWCE/SBW-vectors-300-min5.txt.bz2 \
    && bzip2 -d SBW-vectors-300-min5.txt.bz2 \

RUN wget http://143.107.183.175:22980/download.php?file=embeddings/word2vec/skip_s300.zip \
    && unzip skip_s300.zip \

RUN mkdir falsefriendsp/resources/big \
    && mv SBW-vectors-300-min5.txt falsefriendsp/resources/big/es.txt \
    && mv skip_s300.txt falsefriendsp/resources/big/pt.txt \

EXPOSE 8866

#COPY ./ ./
CMD ["python", "serve.py"]
