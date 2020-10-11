
all:
	$(CXX) cr4ckm3.cpp -o cr4ckm3
	python inputSearchGA.py

cfg: 
	clang++ -emit-llvm -S cr4ckm3.cpp -o cr4ckm3.ll
	opt --dot-cfg cr4ckm3.ll
	dot -Tpng .main.dot -o cr4ckm3.png

clean:
	rm -f ./cr4ckm3 ./cr4ckm3.ll ./cr4ckm3.png  
