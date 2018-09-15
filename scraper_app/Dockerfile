FROM python:3.6-alpine

#RUN apk add --update curl gcc g++ \
#    && rm -rf /var/cache/apk/*

# RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

COPY . /app

WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "./scraper/scraper.py"]
