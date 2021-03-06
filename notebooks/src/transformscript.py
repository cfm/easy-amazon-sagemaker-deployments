<<<<<<< HEAD
import torch
import torch.distributed as dist
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.utils.data
import torch.utils.data.distributed
=======
import gluonnlp as nlp; import mxnet as mx;
>>>>>>> b185640d47582d52e12ce5440adb8cdfe66bbe0a
from joblib import load
import numpy as np
import os
import json
<<<<<<< HEAD
from six import BytesIO

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.conv2_drop = nn.Dropout2d()
        self.fc1 = nn.Linear(320, 50)
        self.fc2 = nn.Linear(50, 10)

    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)
    
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#Return loaded model
def load_model(modelpath):
    model = torch.nn.DataParallel(Net())
    with open(os.path.join(modelpath, 'model.pth'), 'rb') as f:
        model.load_state_dict(torch.load(f))
    print("loaded")
    return model.to(device)

# return prediction based on loaded model (from the step above) and an input payload
def predict(model, payload):
    
    if type(payload) == list:
        data = np.frombuffer(payload[0]['body'],dtype=np.float32).reshape(1,1,28,28)
    elif type(payload) == np.ndarray:
        data = payload  
    try:
        print(type(data))
        input_data = torch.Tensor(data)
        model.eval()
        with torch.no_grad():
            out =  model(input_data.to(device)).argmax(axis=1)[0].tolist()
    except Exception as e:
        out = str(e)
    return [out]
=======

#Return loaded model
def load_model(modelpath):
    model, vocab = nlp.model.get_model('distilbert_6_768_12', dataset_name='distilbert_book_corpus_wiki_en_uncased');
    print("loaded")
    return {'model':model,'vocab':vocab}

# return prediction based on loaded model (from the step above) and an input payload
def predict(modeldict, payload):
    
    #set_trace()
    
    model = modeldict['model']
    vocab = modeldict['vocab']
    
    tokenizer = nlp.data.BERTTokenizer(vocab, lower=True);
    transform = nlp.data.BERTSentenceTransform(tokenizer, max_seq_length=512, pair=False, pad=False);
    
    try:
        # Local
        if type(payload) == str:
            sample = transform(payload);
        elif type(payload) == bytes :
            sample = transform(str(payload.decode()));
        # Remote, standard payload comes in as a list of json strings with 'body' key
        elif type(payload)==list:
            sample = transform(payload[0]['body'].decode());
        else:
            return [json.dumps({'response':"Provide string or bytes string",
                    'payload':str(payload),
                    'type':str(type(payload))})]
        
        words, valid_len = mx.nd.array([sample[0]]), mx.nd.array([sample[1]])
        out = model(words, valid_len)  
        out = json.dumps({'output':out.asnumpy().tolist()})
    except Exception as e:
        out = str(e) #useful for debugging!
    return [out]
>>>>>>> b185640d47582d52e12ce5440adb8cdfe66bbe0a
