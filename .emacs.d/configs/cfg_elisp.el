
(require 'mic-paren)

(add-hook 'emacs-lisp-mode-hook 'paren-activate)
(add-hook 'emacs-lisp-mode-hook 'hs-minor-mode)

(require 'slime)
(slime-setup)
(setq slime-startup-animation nil)

(global-set-key "\C-cs" 'slime-selector)

(add-hook 'lisp-mode-hook 'hs-minor-mode)
(add-hook 'lisp-mode-hook 'slime-mode)
(add-hook 'lisp-mode-hook 'paren-activate)

;(define-key slime-mode-map (kbd "[") 'insert-parentheses)
;(define-key slime-mode-map (kbd "]") 'move-past-close-and-reindent)
(define-key slime-mode-map (kbd "[") (lambda () (interactive) (insert "(")))
(define-key slime-mode-map (kbd "]") (lambda () (interactive) (insert ")")))
(define-key slime-mode-map (kbd "(") (lambda () (interactive) (insert "[")))
(define-key slime-mode-map (kbd ")") (lambda () (interactive) (insert "]")))

;; (define-key slime-mode-map (kbd "C-t") 'transpose-sexps)
;; (define-key slime-mode-map (kbd "C-M-t") 'transpose-chars)
;; (define-key slime-mode-map (kbd "C-b") 'backward-sexp)
;; (define-key slime-mode-map (kbd "C-M-b") 'backward-char)
;; (define-key slime-mode-map (kbd "C-f") 'forward-sexp)
;; (define-key slime-mode-map (kbd "C-M-f") 'forward-char)
