;;BruceXin .emacs file
;;See also 
;;
;;

;;use UTF-8
(prefer-coding-system 'utf-8)
(setq default-enable-multibyte-characters t)


(setq load-path (cons "~/.emacs.d" load-path))
(setq load-path (cons "~/.emacs.d/vendor" load-path))
(setq load-path (cons "~/.emacs.d/vendor/color-theme" load-path))
(setq load-path (cons "~/.emacs.d/vendor/dired" load-path))
(setq load-path (cons "~/.emacs.d/vendor/yasnippet" load-path))
(setq load-path (cons "~/.emacs.d/vendor/anything" load-path))
(setq load-path (cons "~/.emacs.d/vendor/python-mode" load-path))
(setq load-path (cons "~/.emacs.d/vendor/magit" load-path))
(setq load-path (cons "~/.emacs.d/vendor/emhacks" load-path))
(setq load-path (cons "~/.emacs.d/vendor/rfcview" load-path))

(defconst emacs-config-dir "~/.emacs.d/configs/" "")
 
(defun load-cfg-files (filelist)
  (dolist (file filelist)
    (load (expand-file-name
           (concat emacs-config-dir file)))
    (message "Loaded config file: %s" file)
    ))
 
(load-cfg-files '("cfg_main"
                  "cfg_editor"
                  "cfg_ecb"
                  "cfg_yasnippet"
                  "cfg_abbrev"
                  ;"cfg_mmm_mode"
                  "cfg_python"
                  "cfg_theme"
                  "cfg_anything"
                  "cfg_dired"
                  "cfg_git"
                  "cfg_highlight_line"
                  ;"cfg_pair"                  
                  "cfg_rfc"
                  "cfg_session"
                  ))

(custom-set-variables
  ;; custom-set-variables was added by Custom.
  ;; If you edit it by hand, you could mess it up, so be careful.
  ;; Your init file should contain only one such instance.
  ;; If there is more than one, they won't work right.
;; '(ecb-layout-name "left9")
;; '(ecb-maximize-ecb-window-after-selection t)
 '(ecb-options-version "2.32")
;; '(ecb-source-path (quote (("/" "/"))))
;; '(ecb-tip-of-the-day nil)
;; '(ecb-windows-width 0.2)
;;  '(erc-beep-match-types (quote (current-nick keyword)))
;;  '(erc-default-sound "/home/ryan/.emacs.d/sounds/combeep4a.wav")
;;  '(erc-keywords (quote ("Enigma")))
;;  '(erc-match-mode t)
;;  '(erc-modules (quote (button completion fill irccontrols log netsplit noncommands readonly ring scrolltobottom services smiley track)))
;;  '(erc-play-sound t)
;;  '(erc-prompt-for-nickserv-password nil)
;;  '(erc-prompt-for-password t)
;;  '(erc-services-mode t)
;;  '(erc-sound-mode t)
;;  '(erc-sound-path (quote ("/home/ryan/.emacs.d/sounds")))
;;  '(erc-user-full-name "")
 '(fill-column 81)
;;   '(jde-complete-function (quote jde-complete-in-line))
;;   '(jde-jdk (quote ("1.6.0")))
;;   '(jde-jdk-registry (quote (("1.6.0" . "/etc/opt/java"))))
;;   '(jde-sourcepath (quote ("/etc/opt/java/src" "$SDN_ROOT/src/java/")))
 '(mouse-wheel-mode t)
 '(paren-match-face (quote paren-face-match-light))
 '(paren-sexp-mode t)
;; '(w3m-default-display-inline-images t)
 )
(custom-set-faces
  ;; custom-set-faces was added by Custom.
  ;; If you edit it by hand, you could mess it up, so be careful.
  ;; Your init file should contain only one such instance.
  ;; If there is more than one, they won't work right.
 )

