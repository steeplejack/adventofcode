#!sbcl --script

(load "~/.quicklisp/setup.lisp")

(ql:quickload "split-sequence")

(defun diff (lst)
    (if (or (endp lst) (endp (rest lst)))
        nil
        (cons (- (second lst) (first lst)) (diff (rest lst)))))

(defun all-same (lst)
    (if (or (endp lst) (endp (rest lst)))
        t
        (if (eq (first lst) (second lst))
            (all-same (rest lst))
            nil)))

(defun last-elem (lst)
    (first (last lst)))

(defun nextval-recursive (seq acc)
    (if (all-same seq)
        (+ acc (last-elem seq))
        (nextval-recursive (diff seq) (+ acc (last-elem seq)))))

(defun next-val (seq)
    (nextval-recursive seq 0))

(defun prev-val (seq)
    (nextval-recursive (reverse seq) 0))

(defun sum-sequence (seq)
    (reduce #'+ seq :initial-value 0))

(defvar part1
    (sum-sequence (with-open-file (stream "/Users/kg8/code/aoc/2023/day9/input.txt" :direction :input)
        (loop for line = (read-line stream nil)
            while line
            collect (next-val
                (map 'list #'parse-integer
                    (split-sequence:split-sequence #\Space line)))))))

(defvar part2 
    (sum-sequence (with-open-file (stream "/Users/kg8/code/aoc/2023/day9/input.txt" :direction :input)
        (loop for line = (read-line stream nil)
            while line
            collect (prev-val
                (map 'list #'parse-integer
                    (split-sequence:split-sequence #\Space line)))))))


(format t "Part 1: ~A~%" part1)
(format t "Part 2: ~A~%" part2)