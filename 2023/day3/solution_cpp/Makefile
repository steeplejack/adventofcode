.PHONY: clean

build:
	cmake -B build -S .
	cmake --build build/

part1: build
	./build/part1 ../input.txt

part2: build
	./build/part2 ../input.txt

run: part1 part2

clean:
	rm -rf build
