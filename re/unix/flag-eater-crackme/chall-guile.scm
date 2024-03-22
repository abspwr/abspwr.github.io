(use-modules (srfi srfi-1)) ; iota
;(use-modules (srfi srfi-4)) ; vectors, not needed
(use-modules (rnrs bytevectors)) ; #vu8 needed
(use-modules (ice-9 format))

(define magic-bytes #vu8(#x06 #x00 #x00 #x00 #x06 #x00 #x00 #x00 #x30 #x00 #x00 #x00 #x33 #x00 #x00 #x00 #x07 #x00 #x00 #x00 #x07 #x00 #x00 #x00 #x03 #x00 #x00 #x00 #x07 #x00 #x00 #x00 #x32 #x00 #x00 #x00 #x06 #x00 #x00 #x00 #x03 #x00 #x00 #x00 #x05 #x00 #x00 #x00 #x35 #x00 #x00 #x00 #x03 #x00 #x00 #x00 #x05 #x00 #x00 #x00 #x07 #x00 #x00 #x00 #x07 #x00 #x00 #x00 #x07 #x00 #x00 #x00 #x06 #x00 #x00 #x00 #x36 #x00 #x00 #x00 #x07 #x00 #x00 #x00 #x05 #x00 #x00 #x00 #x06 #x00 #x00 #x00 #x06 #x00 #x00 #x00 #x03 #x00 #x00 #x00 #x05 #x00 #x00 #x00 #x03 #x00 #x00 #x00 #x07 #x00 #x00 #x00 #x30 #x00 #x00 #x00 #x07 #x00 #x00 #x00))

(define min-char 32)
(define max-char 127)
(define key-len 30)

(define (is-prime? n)
  (let loop ((i 2))
    (cond ((> (* i i) n) #t)
	  ((= (modulo n i) 0) #f)
	  (else (loop (+ i 1))))))

(define (valid-char? c n) 
  (let ((c (char->integer c)))
    (or (and (not (is-prime? c)) (= (ash c -4) (bytevector-u32-ref magic-bytes (ash n 2) (endianness little))))
	(and (is-prime? c) (= (ash c -1) (bytevector-u32-ref magic-bytes (ash n 2) (endianness little)))))))
      
(define (generate-valid-chars)
  (let ((result (map (lambda (x) '()) (iota 30))))
    (do ((i 0 (+ i 1)))
	((= i key-len))
      (do ((j min-char (+ j 1)))
	  ((= j max-char))
	(when (valid-char? (integer->char j) i)
	  (list-set! result i (append (list-ref result i) (list j)))
	  ;(display (integer->char j))
	  )))
    result))

; ty chatgpt for this function
(define (generate-combinations lst max)
  (let ((kcount 0))
  (define (generate-combinations-helper i result)
    (cond
     ((= kcount max) (exit)) ; limit
     ((= i 30) (format #t "~a~%" (list->string result)) (set! kcount (1+ kcount)))
     (else
      (for-each (lambda (x)
                  (generate-combinations-helper (+ 1 i)
                                                (append result (list (integer->char x)))))
                (list-ref lst i)))))
  (generate-combinations-helper 0 '())))

(define max-keys 1000)
(define valid-chars (generate-valid-chars))
(generate-combinations valid-chars max-keys)

;;; tests

;; (define total-valid-keys (apply * (map (lambda (x) (length x)) valid-chars)))
;; (display total-valid-keys)
; possible key combinations: 522080336425412505336307712

;; (display (is-prime? 17))
;; (display magic-bytes)
;; (display (is-prime? 113))

;; (display (valid-char? #\o 0))
;; (display (valid-char? #\o 1))
;; (display (valid-char? #\~ 4))
;; (display (valid-char? #\a 2))

;; (display (char->integer #\~))
;; (display (integer->char 126))

;; (display (is-prime? 111))

;; (generate-valid-chars)
;; (display (generate-valid-chars))
;(display valid-chars)
