import torch

def print_hi():
	print('hi')

def print_hello():
	print('hello')

def synthetic_data(w,b,num_examples):
    X = torch.normal(0,1,(num_examples,len(w)))
    y = torch.matmul(X,w)+b
    y+=torch.normal(0,0.01,y.shape)
    return X,y.reshape((-1,1))

if __name__=='__main__':
	print_hi()