FROM python
WORKDIR /bitcoinbot
ADD . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]