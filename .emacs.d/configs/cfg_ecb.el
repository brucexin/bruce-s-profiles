(load-file "/usr/share/emacs/site-lisp/cedet/common/cedet.el")
     (semantic-load-enable-code-helpers)
     (autoload 'speedbar-frame-mode "speedbar" "Popup a speedbar frame" t)
     (autoload 'speedbar-get-focus "speedbar" "Jump to speedbar frame" t)
     (define-key-after (lookup-key global-map [menu-bar tools])
                [speedbar]
                '("Speedbar" .
                speedbar-frame-mode)
                [calendar])

;;semantic setting
(setq semantic-load-turn-everything-on t)
(require 'semantic)
(require 'semantic-load)
(require 'semantic-ia)
(require 'semanticdb)
(setq-default semanticdb-project-roots
              (list (expand-file-name "/")))
(setq-default semanticdb-persistent-path
              (list (expand-file-name "~/.emacs_tmp/semanticdb")))
(setq-default semanticdb-default-save-direc×y
              (expand-file-name "~/.emacs_tmp/semanticdb"))
(setq-default semanticdb-default-system-save-direc×y
              (expand-file-name "~/.emacs_tmp/semanticdb"))

(global-semanticdb-minor-mode 1)
;;(add-hook 'speedbar-load-hook (lambda () (require 'semantic-sb)))
(require 'semantic-sb)
(add-hook 'semantic-init-hooks (lambda ()
                                 (imenu-add-to-menubar "TOKENS")))
(setq-default semantic-idle-scheduler-idle-time 432000) ;不加这句cpu会飞到100%

;(load-file "/usr/share/emacs/site-lisp/cedet/common/cedet.el")
(semantic-load-enable-minimum-features)
;;;;C/C++语言启动时自动加载semantic对/usr/include的索引数据库
(setq semanticdb-search-system-databases t)
  (add-hook 'c-mode-common-hook
          (lambda ()
            (setq semanticdb-project-system-databases
                  (list (semanticdb-create-database
                           semanticdb-new-database-class
                           "/usr/include")))))

;;(setq-default abbrev-mode t)
(autoload 'senator-try-expand-semantic "senator")
(setq hippie-expand-try-functions-list
      '(
        senator-try-expand-semantic
        try-expand-dabbrev
        try-expand-dabbrev-visible
        try-expand-dabbrev-all-buffers
        try-expand-dabbrev-from-kill
        try-complete-file-name-partially
        try-complete-file-name
        try-expand-all-abbrevs
        try-expand-line
        try-expand-list
        try-expand-line-all-buffers
        try-expand-list-all-buffers
        try-expand-whole-kill))
(global-set-key (kbd "C-/") 'hippie-expand)
(global-set-key (kbd "M-/") 'semantic-ia-complete-symbol)


;; ecb设置
(add-to-list 'load-path
	     "/usr/share/emacs/site-lisp/ecb")
(load-file "/usr/share/emacs/site-lisp/ecb/ecb.el")
(require 'ecb)
(setq ecb-auto-activate nil
          ecb-tip-of-the-day nil
          ecb-tree-indent 4
          ecb-windows-height 0.5
          ecb-windows-width 0.2
          ecb-auto-compatibility-check nil
          ecb-version-check nil
          ecb-layout-name "left-dir-plus-speedbar"
          inhibit-startup-message t)
