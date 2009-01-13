;; Change the abbreviation table on the fly depending on mode
;; as well as if we are in a comment or quoted string
;; (require 'pabbrev)
;; (add-hook 'pre-abbrev-expand-hook 'abbrev-table-change)
;; (defun abbrev-table-change (&optional args)
;;   (setq local-abbrev-table
;;         (if (eq major-mode 'python-mode)
;;             (if (py-in-literal)
;;                 text-mode-abbrev-table
;;               python-mode-abbrev-table)
;;         )
;;   )
;; )

;; predictive install location
(add-to-list 'load-path "~/.emacs.d/vendor/predictive/")
;; dictionary locations
(add-to-list 'load-path "~/.emacs.d/vendor/predictive/latex/")
(add-to-list 'load-path "~/.emacs.d/vendor/predictive/html/")
(setq predictive-auto-complete t)
;; load predictive package
;; (autoload 'predictive-mode "~/.emacs.d/predictive/"
;;   "Turn on Predictive Completion Mode." t
;; load predictive package
(require 'predictive)
