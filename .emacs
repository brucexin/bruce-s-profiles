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
                  "cfg_pair"
                  "cfg_session"
                  ))
