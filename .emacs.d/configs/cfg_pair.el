(setq skeleton-end-hook nil) ; do not insert newline after skeleton insertation

(defvar myskeleton-pairs
  '((?\" . (?\" ?\" ?\" _ ?\"))
    (?\( . (?\( ?\) ?\( _ ?\)))
    (?\[ . (?\[ ?\] ?\[ _ ?\]))
    (?\{ . (?\{ ?\} ?\{ _ ?\}))
    (?\' . (?\' ?\' ?\' _ ?\'))
    (?\` . (?\` ?\' ?\` _ ?\')))
  "Table of skeletons pairs. Maybe local to buffer.")

(defun myskeleton-pair-insert (arg)
  "Inserts pairs."
  (interactive "*P")

  (let* ((chr (event-key last-command-event))
         (pair (assoc chr myskeleton-pairs)))
    (if (null pair)
        (message "Character %s is not in `myskeleton-pairs'.")
      (cond ((and (listp arg) (not (null arg)))
    		 ;; Surraund current word with
    		 (save-excursion
    		   (when (not (looking-at "\\<"))
    		     (backward-word 1))
    		   (when (looking-at "\\sw")
    		     (let ((pl 0)
                       (r (prefix-numeric-value arg)))
    		       (while (> r 1)
                     (setq r (/ r 4))
                     (setq pl (1+ pl)))

    		       (insert (make-string pl (nth 0 (cdr pair))))
    		       (forward-word 1)
    		       (insert (make-string pl (nth 1 (cdr pair))))))))
            (t (mapcar (lambda (not-used)
                         (skeleton-insert
                          (cons nil (cdddr pair))))
                       (make-list (prefix-numeric-value arg) 'not-used)))))))

;; (define-key global-map (kbd "C-M-{") 'backward-paragraph)
;; (define-key global-map (kbd "C-M-}") 'forward-paragraph)
;; (define-key global-map (kbd "C-M-'") 'abbrev-prefix-mark)

(define-key global-map (kbd "\"") 'myskeleton-pair-insert)
(define-key global-map (kbd "`") 'myskeleton-pair-insert)
(define-key global-map (kbd "'") 'myskeleton-pair-insert)
(define-key global-map (kbd "{") 'myskeleton-pair-insert)
(define-key global-map (kbd "(") 'myskeleton-pair-insert)
(define-key global-map (kbd "[") 'myskeleton-pair-insert)

(add-hook 'c-mode-hook 'myskeleton-pair-insert)
(add-hook 'c++-mode-hook 'myskeleton-pair-insert)
(add-hook 'python-mode-hook 'myskeleton-pair-insert)
