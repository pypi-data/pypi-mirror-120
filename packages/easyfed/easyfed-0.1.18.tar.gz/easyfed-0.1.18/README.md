# An Easy federated learning for any pytorch ML model
you can easely federated training any pytorch model by this tools

## step 1 :
same as server and client

```sh
pip install easyfed -U
```

## step 2 :
open a terminal start server service:

```sh
>>easyfed_server -port=16668
```

## step 3:
the client define client

```python
from easyfed import client
client=client('clientname','http://xx.xx.xx.xx:16668')
```

## step 4:
submit the client model weights to server and exchange
    import numpy
    import torch
    from torch import nn
    class MLP(nn.Module):
        def __init__(self):
            super(MLP, self).__init__()
            self.input = nn.Linear(8, 32)
            self.hidden = nn.Linear(32, 16)
            self.relu=nn.ReLU(inplace=True)
            self.fc1 = nn.Linear(16, 2)
            self.softmax = nn.Softmax()
            self.cross_entropy=nn.CrossEntropyLoss()
        def forward(self, x,y):
            x = self.input(x)               # Batch_size * Embed_dim(128)
            x=self.hidden(x)
            x = self.fc1(self.relu(x))                 # Batch_size * Hidden(128)
            score=self.softmax(x)
            loss=self.cross_entropy(x,y)
            return score,loss

```python
dataset = numpy.loadtxt("pima-indians-diabetes.csv", delimiter=",")
X = dataset[:,0:8]
Y = dataset[:,8]
model=MLP()
optimizer=torch.optim.SGD(model.parameters(), lr=0.1,momentum=0.5) 

for epoch in range(10000):
    if epoch>0 and epoch%100==0:
        model=client.submit(model,loss.item()) # when each 100 epoch submit the model and get the server aggregated model weights
    optimizer.zero_grad()
    x=torch.tensor(X,dtype=torch.float)
    score,loss=model(x,torch.tensor(Y,dtype=torch.long))
    loss.backward()
    optimizer.step()
```
