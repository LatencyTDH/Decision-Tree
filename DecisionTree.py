# DecisionTree.py
# ----------------
# Modified by: Sean Dai
# CS 3600: Project 4a

from math import log
from collections import Counter
import sys

class Node:
  """
  A simple node class to build our tree with. It has the following:
  
  children (dictionary<str,Node>): A mapping from attribute value to a child node
  attr (str): The name of the attribute this node classifies by. 
  islead (boolean): whether this is a leaf. False.
  """
  
  def __init__(self,attr):
    self.children = {}
    self.attr = attr
    self.isleaf = False

class LeafNode(Node):
    """
    A basic extension of the Node class with just a value.
    
    value (str): Since this is a leaf node, a final value for the label.
    islead (boolean): whether this is a leaf. True.
    """
    def __init__(self,value):
        self.value = value
        self.isleaf = True
    
class Tree:
  """
  A generic tree implementation with which to implement decision tree learning.
  Stores the root Node and nothing more. A nice printing method is provided, and
  the function to classify values is left to fill in.
  """
  def __init__(self, root=None):
    self.root = root

  def prettyPrint(self):
    print str(self)
    
  def preorder(self,depth,node):
    if node is None:
      return '|---'*depth+str(None)+'\n'
    if node.isleaf:
      return '|---'*depth+str(node.value)+'\n'
    string = ''
    for val in node.children.keys():
      childStr = '|---'*depth
      childStr += '%s = %s'%(str(node.attr),str(val))
      string+=str(childStr)+"\n"+self.preorder(depth+1, node.children[val])
    return string    

  def count(self,node=None):
    if node is None:
      node = self.root
    if node.value is not None:
      return 1
    count = 1
    for child in node.children.values():
      if child is not None:
        count+= self.count(child)
    return count  

  def __str__(self):
    return self.preorder(0, self.root)
  
  def classify(self, classificationData):
    """
    Uses the classification tree with the passed in classificationData.`
    
    Args:
        classificationData (dictionary<string,string>): dictionary of attribute values
    Returns:
        str
        The classification made with this tree.
    """
    #YOUR CODE HERE
    node = self.root

    while not node.isleaf:
        attribute = node.attr
        node = node.children[classificationData[attribute]]
    return node.value



def getPertinentExamples(examples,attrName,attrValue):
    """
    Helper function to get a subset of a set of examples for a particular assignment 
    of a single attribute. That is, this gets the list of examples that have the value 
    attrValue for the attribute with the name attrName.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrName (str): the name of the attribute to get counts for
        attrValue (str): a value of the attribute
        className (str): the name of the class
    Returns:
        list<dictionary<str,str>>
        The new list of examples.
    """
    newExamples = []
    #YOUR CODE HERE

    for exampleDict in examples:
        if attrName in exampleDict and attrValue == exampleDict[attrName]:
            newExamples.append(exampleDict)
    return newExamples
  
def getClassCounts(examples,className):
    """
    Helper function to get a list of counts of different class values
    in a set of examples. That is, this returns a list where each index 
    in the list corresponds to a possible value of the class and the value
    at that index corresponds to how many times that value of the class 
    occurs.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        className (str): the name of the class
    Returns:
        dictionary<string,int>
        This is a dictionary that for each value of the class has the count
        of that class value in the examples. That is, it maps the class value
        to its count.
    """

    classCounts = Counter()
    #YOUR CODE HERE
    for i in xrange(len(examples)):
        classCounts[examples[i][className]] += 1

    return classCounts

def getMostCommonClass(examples,className):
    """
    A freebie function useful later in makeSubtrees. Gets the most common class
    in the examples. See parameters in getClassCounts.
    """
    counts = getClassCounts(examples,className)
    return max(counts, key=counts.get) if len(examples)>0 else None

def getAttributeCounts(examples,attrName,attrValues,className):
    """
    Helper function to get a list of counts of different class values
    corresponding to every possible assignment of the passed in attribute. 
  That is, this returns a list of lists, where each index in the list
  corresponds to an assignment of the attribute named attrName and holds
  the counts of different class values for the subset of the examples
  that have that assignment of that attribute.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrName (str): the name of the attribute to get counts for
        attrValues (list<str>): list of possible values for attribute
        className (str): the name of the class
    Returns:
        list<list<int>>
        This is a list that for each value of the attribute has a
        list of counts of class values. No specific ordering of the
        classes in each list is needed.
    """
    counts=[]
    #YOUR CODE HERE

    for val in attrValues:
        attr_val_counts = []
        class_counts = getClassCounts(getPertinentExamples(examples, attrName, val), className)
        for key in class_counts:
            attr_val_counts.append(class_counts[key])
        counts.append(attr_val_counts)

    return counts
        

def setEntropy(classCounts):
    """
    Calculates the set entropy value for the given list of class counts.
    This is called H in the book. Note that our labels are not binary,
    so the equations in the book need to be modified accordingly. Note
    that H is written in terms of B, and B is written with the assumption 
    of a binary value. B can easily be modified for a non binary class
    by writing it as a summation over a list of ratios, which is what
    you need to implement.
    
    Args:
        classCounts (list<int>): list of counts of each class value
    Returns:
        float
        The set entropy score of this list of class value counts.
    """
    #YOUR CODE HERE

    calculateUncertainty = lambda x: x/total * log(x/total, 2)
    total = float(sum(classCounts))

    return -1 * sum(map(calculateUncertainty, classCounts))
   

def remainder(examples,attrName,attrValues,className):
    """
    Calculates the remainder value for given attribute and set of examples.
    See the book for the meaning of the remainder in the context of info 
    gain.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrName (str): the name of the attribute to get remainder for
        attrValues (list<string>): list of possible values for attribute
        className (str): the name of the class
    Returns:
        float
        The remainder score of this value assignment of the attribute.
    """
    #YOUR CODE HERE
    remainder_value = 0.0
    attrCounts = getAttributeCounts(examples, attrName, attrValues, className)
    total = sum(map(sum, attrCounts), 0.0)

    for trainingSubset in attrCounts:
        if trainingSubset and total not in trainingSubset:
                remainder_value += sum(trainingSubset)/total * setEntropy(trainingSubset)

    return remainder_value
          
def infoGain(examples,attrName,attrValues,className):
    """
    Calculates the info gain value for given attribute and set of examples.
    See the book for the equation - it's a combination of setEntropy and
    remainder (setEntropy replaces B as it is used in the book).
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrName (str): the name of the attribute to get remainder for
        attrValues (list<string>): list of possible values for attribute
        className (str): the name of the class
    Returns:
        float
        The gain score of this value assignment of the attribute.
    """
    #YOUR CODE HERE

    classCounts = getClassCounts(examples, className)
    classCounts = [val for val in classCounts.values()]
    return setEntropy(classCounts) - remainder(examples, attrName, attrValues, className)
  
def giniIndex(classCounts):
    """
    Calculates the gini value for the given list of class counts.
    See equation in instructions.
    
    Args:
        classCounts (list<int>): list of counts of each class value
    Returns:
        float
        The gini score of this list of class value counts.
    """
    #YOUR CODE HERE
    freq_square = lambda x: (x/total) ** 2
    total = sum(classCounts, 0.0)
    return 1 - sum(map(freq_square, classCounts))
  
def giniGain(examples,attrName,attrValues,className):
    """
    Return the inverse of the giniD function described in the instructions.
    The inverse is returned so as to have the highest value correspond 
    to the highest information gain as in entropyGain. If the sum is 0,
    return sys.maxint.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrName (str): the name of the attribute to get counts for
        attrValues (list<string>): list of possible values for attribute
        className (str): the name of the class
    Returns:
        float
        The summed gini index score of this list of class value counts.
    """
    #YOUR CODE HERE
    score = 0.0
    attrCounts = getAttributeCounts(examples, attrName, attrValues, className)
    total = sum(map(sum, attrCounts), 0.0)

    for trainingSubset in attrCounts:
        if trainingSubset:
                score += sum(trainingSubset)/total * giniIndex(trainingSubset)

    if score == 0:
        return sys.maxint

    return 1.0 / score
    
def makeTree(examples, attrValues,className,setScoreFunc,gainFunc):
    """
    Creates the classification tree for the given examples. Note that this is implemented - you
    just need to imeplement makeSubtrees.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrValues (dictionary<string,list<string>>): list of possible values for attribute
        className (str): the name of the class
        classScoreFunc (func): the function to score classes (ie setEntropy or giniIndex)
        gainFunc (func): the function to score gain of attributes (ie infoGain or giniGain)
    Returns:
        Tree
        The classification tree for this set of examples
    """
    remainingAttributes=attrValues.keys()
    return Tree(makeSubtrees(remainingAttributes,examples,attrValues,className,setScoreFunc,gainFunc))
    
def makeSubtrees(remainingAttributes,examples,attributeValues,className,setScoreFunc,gainFunc, parents=None):
    """
    Creates a classification tree Node and all its children. This returns a Node, which is the root
    Node of the tree constructed from the passed in parameters. This should be implemented recursively,
    and handle base cases for zero examples or remainingAttributes as covered in the book.    

    Args:
        remainingAttributes (list<string>): the names of attributes still not used
        examples (list<dictionary<str,str>>): list of examples
        attrValues (dictionary<string,list<string>>): list of possible values for attribute
        className (str): the name of the class
        setScoreFunc (func): the function to score classes (ie classEntropy or gini)
        gainFunc (func): the function to score gain of attributes (ie entropyGain or giniGain)
    Returns:
        Node or LeafNode
        The classification tree node optimal for the remaining set of attributes.
    """
    #YOUR CODE HERE

    if not examples:
        return LeafNode(getMostCommonClass(parents, className))
    elif checkAllSameClassification(examples, className):
        return LeafNode(examples[0][className])
    elif not remainingAttributes:  # indicates noise in data
        return LeafNode(getMostCommonClass(examples, className))
    else:
        bestAttribute = bestSplit(examples, remainingAttributes, attributeValues, className, gainFunc)
        root = Node(bestAttribute)
        # Create a new decision tree for each value in bestAttribute
        for val in attributeValues[bestAttribute]:
            exs = getPertinentExamples(examples, bestAttribute, val)
            newRemaining = [x for x in remainingAttributes if x != bestAttribute]
            subtree = makeSubtrees(newRemaining, exs, attributeValues, className, setScoreFunc, gainFunc, examples)
            root.children[val] = subtree
        return root

def checkAllSameClassification(examples, className):
    """
    Returns true if examples have the same classification

    :param examples: (list<dictionary<str,str>>): list of examples
    :param className: (str): the name of the class
    :return: True if examples have the same classification
    """
    class_to_check = examples[0][className]
    return all(example[className] == class_to_check for example in examples)

def bestSplit(examples, attrNames, attrValues, className, gainFunc):
    """
    Selects the best attribute by which to split the decision tree by calculating
    the score gain of each attribute.

    :param examples: (list<dictionary<str,str>>): list of examples
    :param attrNames: (list<string>): the names of attributes still not used
    :param attrValues: (dictionary<string,list<string>>): list of possible values for attribute
    :param className: (str): the name of the class
    :param gainFunc: lambda that calculates information gain
    :return: attribute (str): name of attribute with the most information gain
    """
    best = ("", ~sys.maxint)
    #calculates gain for each attribute
    for attrName in attrNames:
        gain = gainFunc(examples, attrName, attrValues[attrName], className)
        if gain > best[1]:
            best = (attrName, gain)
    return best[0]
