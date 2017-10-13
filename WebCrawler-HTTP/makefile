JFLAGS = -cp
JC = javac
JARFILE = "./jsoup-1.8.3.jar"

.SUFFIXES: .java .class

.java.class:
	$(JC) $(JFLAGS) $(JARFILE):./ $*.java

CLASSES = \
	PersistentCrawl.java 

default: classes

classes: $(CLASSES:.java=.class)

clean:
	$(RM) *.class
