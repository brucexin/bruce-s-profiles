(setq rfc-url-save-directory "~/rfc")
(setq rfc-index-url "http://www.ietf.org/iesg/1rfc_index.txt")
(setq rfc-archive-alist (list (concat rfc-url-save-directory "/rfc.zip")
                              rfc-url-save-directory
                              "http://www.ietf.org/rfc/"))
(setq rfc-insert-content-url-hook '(rfc-url-save))
(require 'rfc)

(setq auto-mode-alist
      (cons '("/rfc[0-9]+\\.txt\\(\\.gz\\)?\\'" . rfcview-mode)
            auto-mode-alist))

(autoload 'rfcview-mode "rfcview" nil t)

(eval-after-load "speedbar" '(load-library "sb-rfcview"))
(custom-set-variables
 '(speedbar-supported-extension-expressions
   (append
    speedbar-supported-extension-expressions
    '("rfc[0-9]+\\.txt"))))

