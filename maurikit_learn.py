import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import plot_confusion_matrix as confusion_matrix

class LogisticRegression_GRAD():
    def __init__(self):
        self._estimator_type = "classifier"
        pass
    
    def fit(self, X, y, epochs=30, learning_rate=0.02):
        #Custo
        self.custos = np.array([])
        
        #Bias
        bias = np.ones((X.shape[0], 1))
        X = np.hstack((bias,X))
        self.w = np.ones(X.shape[1])
        print(self.w)
            
        for i in range(0, epochs):
            #Y predito
            y_pred = np.array([])
            for j in range(0, X.shape[0]):
                y_pred = np.append(y_pred, 1 / (1 + np.exp(np.sum((-1) * np.transpose(self.w) * X[j]))))
            
            #Calculo do Somatório(ei * xi)
            exi = 0     
            for j in range(0, X.shape[0]):
                exi += (y[j] - y_pred[j]) * X[j] #Correção no gradiente
            exi_n = (exi/X.shape[0])
            
            #Atualização dos pesos
            self.w = self.w + (learning_rate * exi_n)
            
            #Calcula e salva custo
            custo = np.sum((-1) * np.log(y_pred) - (1 - y) * np.log(1 - y_pred)) / X.shape[0] * 2
            self.custos = np.append(self.custos, custo)

        print("Coeficientes: " + str(self.w))
                          
    def predict(self, X):
        result = np.array([])
        y_pred = np.array([])
        for j in range(0, X.shape[0]):
            y_pred = np.append(y_pred, 1 / (1 + np.exp((-1) * self.w[0] + np.sum((-1) * np.transpose(self.w[1:]) * X[j]))))
                
        for i in y_pred:
            if i < 0.5:
                result = np.append(result, 0)
            else:
                result = np.append(result, 1)
                      
        return result

class Classification_NBG():
    def __init__(self):
        self._estimator_type = "classifier"
        pass
    
    def fit(self, X, y):
        self.classes_probabilidades = {}
        self.classes_medias = {}
        
        self.E = np.cov(X, rowvar=False)
        self.classes, classes_qtds =  np.unique(y, return_counts=True)
        
        for classe, classe_qtd in zip(self.classes, classes_qtds):
            indices = np.where(y == classe)
            self.classes_probabilidades[classe] = (classe_qtd / X.shape[0])
            x = np.array([X[index, :] for index in indices]).reshape(classe_qtd, X.shape[1])
            self.classes_medias[classe] = x.mean(axis=0)

    def predict(self, X):
        result = np.array([])
        for x in X:
            x_result = np.array([])
            for classe in self.classes:
                aux = 1 / np.sqrt(np.linalg.det(self.E)) * ((2*np.pi) ** (X.shape[1] / 2))
                prob_xc = aux * np.exp(-(1.0/2) * np.transpose(x - self.classes_medias[classe]) @ np.linalg.inv(self.E) @ (x - self.classes_medias[classe]))
                x_result = np.append(x_result, prob_xc * self.classes_probabilidades[classe])
            melhor_classe = self.classes[np.where(x_result == x_result.max())]
            result = np.append(result, melhor_classe) 
        return result
    
class Classification_QD():
    def __init__(self):
        self._estimator_type = "classifier"
        pass
    
    def fit(self, X, y):
        self.classes_probabilidades = {}
        self.classes_medias = {}
        self.Es = {}
        self.classes, classes_qtds =  np.unique(y, return_counts=True)
        
        for classe, classe_qtd in zip(self.classes, classes_qtds):
            indices = np.where(y == classe)
            self.classes_probabilidades[classe] = (classe_qtd / X.shape[0])
            x = np.array([X[index, :] for index in indices]).reshape(classe_qtd, X.shape[1])
            self.classes_medias[classe] = x.mean(axis=0)
            self.Es[classe] = np.cov(x, rowvar=False)

    def predict(self, X):
        result = np.array([])
        for x in X:
            x_result = np.array([])
            for classe in self.classes:
                aux = 1 / np.sqrt(np.linalg.det(self.Es[classe])) * ((2*np.pi) ** (X.shape[1] / 2))
                prob_xc = aux * np.exp(-(1.0/2) * np.transpose(x - self.classes_medias[classe]) @ np.linalg.inv(self.Es[classe]) @ (x - self.classes_medias[classe]))
                x_result = np.append(x_result, prob_xc * self.classes_probabilidades[classe])
            melhor_classe = self.classes[np.where(x_result == x_result.max())]
            result = np.append(result, melhor_classe) 
        return result
 
    
def acuracia(y_true, y_pred):
    qtdAcertos = 0
    for i in range(0, y_true.shape[0]):
        if y_true[i] == y_pred[i]:
            qtdAcertos += 1

    return qtdAcertos/y_true.shape[0]


def plot_confusion_matrix(classifier, X_test, y_test):
    class_names = np.unique(y_test)
    np.set_printoptions(precision=2)
    title = "Matriz de Confusão"
    disp = confusion_matrix(classifier, X_test, y_test,
                                 display_labels=class_names,
                                 cmap=plt.cm.Blues,
                                 normalize=None)
    disp.ax_.set_title(title);
    print(title)
    print(disp.confusion_matrix)
    plt.show()


def plot_boundaries(classifier, X, y):
    x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
    y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
    h = 0.02

    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    Z = classifier.predict(np.c_[xx.ravel(), yy.ravel()])

    Z = Z.reshape(xx.shape)
    plt.figure(1, figsize=(4, 3))
    plt.pcolormesh(xx, yy, Z, cmap=plt.cm.Paired)

    plt.scatter(X[:, 0], X[:, 1], c=y, edgecolors='k', cmap=plt.cm.Paired)
    plt.xlabel('X1')
    plt.ylabel('X2')

    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.xticks(())
    plt.yticks(())

    plt.show()


    