;; Other configuration
;Reload .emacs on the fly
(defun reload-dot-emacs()
  (interactive)
  (if(bufferp (get-file-buffer ".emacs"))
      (save-buffer(get-buffer ".emacs")))
  (load-file "~/.emacs")
  (message ".emacs reloaded successfully"))

;; no splash screen
(setq inhibit-startup-message t)

;; allow remote editing through transmit
(setq backup-by-copying t) 

;; make pretty
(global-font-lock-mode 1)
 
;; shows current selected region
(setq-default transient-mark-mode t)

;; indent via spaces not tabs
(setq-default indent-tabs-mode nil)

;; titlebar = buffer unless filename
(setq frame-title-format '(buffer-file-name "%f" ("%b")))

;; show paired parenthasis
(show-paren-mode 1)
 
;(set-default-font "-adobe-courier-bold-o-normal--18-180-75-75-m-110-iso8859-13")

;; TAB => 4*'\b'
(setq default-tab-width 4)

;; line numbers
(load-file "~/.emacs.d/vendor/linum.el")
(global-linum-mode 1)
(setq column-number-mode  t)

;; EOL whitespace
(setq show-trailing-whitespace t)

;; turn off tool bar, and menu bar
(if (fboundp 'tool-bar-mode) (tool-bar-mode -1))
(if (fboundp 'scroll-bar-mode) (scroll-bar-mode -1))

;; Make sure we have font-lock to start with
(require 'font-lock)

;; log the time of the things I have done
(setq-default org-log-done t) 

;; get rid of yes-or-no questions - y or n is enough
(defalias 'yes-or-no-p 'y-or-n-p)
 
(require 'uniquify)
(setq uniquify-buffer-name-style 'reverse)
(setq uniquify-separator "|")
(setq uniquify-after-kill-buffer-p t) ; rename after killing uniquified
(setq uniquify-ignore-buffers-re "^\\*") ; don't muck with special buffers

;; See http://www.delorie.com/gnu/docs/elisp-manual-21/elisp_620.html
;; and http://www.gnu.org/software/emacs/manual/elisp.pdf

;; disable line wrap
;(setq default-truncate-lines nil)

;; make side by side buffers function the same as the main window
(setq truncate-partial-width-windows nil)

;; Add F12 to toggle line wrap
;(global-set-key [f8] 'toggle-truncate-lines)

(custom-set-faces
  ;; custom-set-faces was added by Custom.
  ;; If you edit it by hand, you could mess it up, so be careful.
  ;; Your init file should contain only one such instance.
  ;; If there is more than one, they won't work right.
 '(default ((t (:stipple nil :background "#1e1e27" :foreground "#cfbfad" :inverse-video nil :box nil :strike-through nil :overline nil :underline nil :slant normal :weight semi-light :height 140 :width normal :family "apple-inconsolata-medium"))))
 '(highlight-current-line-face ((t (:background "#000000")))))


;; full screen toggle using command+[RET]
(defun toggle-fullscreen () 
  (interactive) 
  (set-frame-parameter nil 'fullscreen (if (frame-parameter nil 'fullscreen) 
                                           nil 
                                           'fullboth)))
;(global-set-key [(meta return)] 'toggle-fullscreen) 
(global-set-key [f11] 'toggle-fullscreen)

;; bury the buffer
(global-set-key [f8] 'bury-buffer)

;; multi-term
(require 'multi-term)
(multi-term-keystroke-setup) 
(setq multi-term-program "/bin/bash") 

;; gist support for github
(load-file "~/.emacs.d/vendor/gist.el")


;; windmove bindings
(when (fboundp 'windmove-default-keybindings)
      (windmove-default-keybindings))



;; Add in lorem-ipsum
;; (load-file "~/.emacs.d/vendor/lorem-ipsum.el")
;; (add-hook 'sgml-mode-hook (lambda ()
;; 			    (setq Lorem-ipsum-paragraph-separator "<br><br>\n"
;; 				  Lorem-ipsum-sentence-separator "&nbsp;&nbsp;"
;; 				  Lorem-ipsum-list-beginning "<ul>\n"
;; 				  Lorem-ipsum-list-bullet "<li>"
;; 				  Lorem-ipsum-list-item-end "</li>\n"
;; 				  Lorem-ipsum-list-end "</ul>\n")))

(defun sendOmni () 
  (interactive)
  (let ((fname (buffer-file-name (current-buffer))))
	(do-applescript (concat "tell front document of application \"OmniFocus\" 
                set aTask to (make new inbox task with properties {name:\"From Emacs " 
				(buffer-name (current-buffer)) "\", note:\"file:///" fname "  \" })
                    tell note of aTask
		      make new file attachment with properties {file name:\"" fname "\"}
	            end tell
             end tell"))
	))

;; I use F3 for omnifocus clipping...
(global-set-key [f3] 'sendOmni)

;; ========== Place Backup Files in Specific Directory ==========

;; Enable backup files.
(setq make-backup-files t)

;; Enable versioning with default values (keep five last versions, I think!)
(setq version-control t)

;; Save all backup file in this directory.
(setq backup-directory-alist (quote ((".*" . "~/.emacs_tmp/"))))

; stolen from http://github.com/febuiles/dotemacs/tree/master/temp_files.el
(defvar user-temporary-file-directory
  (concat temporary-file-directory user-login-name "/"))
(make-directory user-temporary-file-directory t)
(setq backup-by-copying t)
(setq backup-directory-alist
      `(("." . ,user-temporary-file-directory)
        (,tramp-file-name-regexp nil)))
(setq auto-save-list-file-prefix
      (concat user-temporary-file-directory ".auto-saves-"))
(setq auto-save-file-name-transforms
      `((".*" ,user-temporary-file-directory t)))

;; When things go wrong, turn this on
;(toggle-debug-on-error t)

;(require 'growl)

;设置删除纪录
(setq kill-ring-max 200)
(require 'browse-kill-ring+)
(global-set-key (kbd "s-k") 'browse-kill-ring)

;; IDO rules
(require 'ido)
(ido-mode t)
(setq ido-enable-flex-matching t)

; textmate
;; (add-to-list 'load-path "~/.emacs.d/vendor/textmate")
;; (require 'textmate)
;; (textmate-mode)

;; (add-to-list 'load-path "/usr/local/share/emacs/site-lisp") 
(require 'magit)
(autoload 'magit-status "magit" nil t)

;;;; goto-line
(global-set-key "\C-c\C-g" 'goto-line)

;; Expand any hidden blocks on goto-line
;; (defadvice goto-line (after expand-after-goto-line
;; 														activate compile)

(require 'tabbar)
(tabbar-mode t)
(global-set-key (kbd "C-<") 'tabbar-backward-group)
(global-set-key (kbd "C->") 'tabbar-forward-group)
(global-set-key (kbd "C-,") 'tabbar-backward)
(global-set-key (kbd "C-.") 'tabbar-forward)


;; 	"hideshow-expand affected block when using goto-line in a collapsed buffer"
;; 	(save-excursion
;; 		(hs-show-block)))
