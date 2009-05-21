;; allow remote editing through transmit
(setq backup-by-copying t) 


;; shows current selected region
(setq-default transient-mark-mode t)

;; indent via spaces not tabs
(setq-default indent-tabs-mode nil)

;; TAB => 4*'\b'
(setq default-tab-width 4)

;设置删除纪录
(setq kill-ring-max 200)
(require 'browse-kill-ring+)
(global-set-key (kbd "s-k") 'browse-kill-ring)

;删除整行时连换行符一起删除
(setq-default kill-whole-line t)


;当光标在行尾上下移动的时候，始终保持在行尾。
(setq track-eol t)

;光标靠近鼠标指针时，让鼠标指针自动让开
(mouse-avoidance-mode 'animate)

;; Page down/up move the point, not the screen.
;; In practice, this means that they can move the
;; point to the beginning or end of the buffer.
;; 参见 http://snarfed.org/space/emacs+page+up+page+down
(global-set-key [next]
  (lambda () (interactive)
    (condition-case nil (scroll-up)
      (end-of-buffer (goto-char (point-max))))))

(global-set-key [prior]
  (lambda () (interactive)
    (condition-case nil (scroll-down)
      (beginning-of-buffer (goto-char (point-min))))))

;Always end searches at the beginning of the matching expression.
(defun bsn-goto-match-beginning ()
  "Use with isearch hook to end search at first char of match."
  (when isearch-forward (goto-char isearch-other-end)))
(add-hook 'isearch-mode-end-hook 'bsn-goto-match-beginning)

;支持emacs和外部程序的粘贴
(setq x-select-enable-clipboard t)

;移动整行的功能
;meta+箭头移动行
;参见 https://svn.rizoma.cl/svn/emacswiki/MoveLine
(defun move-line (n)
  "Move the current line up or down by N lines."
  (interactive "p")
  (setq col (current-column))
  (beginning-of-line) (setq start (point))
  (end-of-line) (forward-char) (setq end (point))
  (let ((line-text (delete-and-extract-region start end)))
    (forward-line n)
    (insert line-text)
    ;; res×e point to original column in moved line
    (forward-line -1)
    (forward-char col)))

(defun move-line-up (n)
  "Move the current line up by N lines."
  (interactive "p")
  (move-line (if (null n) -1 (- n))))

(defun move-line-down (n)
  "Move the current line down by N lines."
  (interactive "p")
  (move-line (if (null n) 1 n)))
(global-set-key (kbd "M-<up>") 'move-line-up)
(global-set-key (kbd "M-<down>") 'move-line-down)

;;这个功能就是根据光标的所在位置，智能的选择一块区域，也就
;;是设置成为当前的 point 和 mark。这样就可以方便的拷贝或者剪切，或者交换他们的位
;;置。
;;如果当前光标在一个单词上，那么区域就是这个单词的开始和结尾分别。
;;如果当前光标在一个连字符上，那么就选择包含连字符的一个标识符。
;;这个两个的是有区别的，而且根据不同的 mode 的语法定义，连字符和单词的定义也不一样。
;;例如 C mode 下， abc_def_xxx , 如果光标停在 abc 上，那么就会选择 abc 这个单词。 如果
;;停在下划线上，那么就会选择 abc_def_xxx 。
;;如果当前光标在一个双引号,单引号，一个花括号，方括号，圆括号，小于号，或者大于号，
;;等等，那么就会选择他们对应的另一个括号之间的区域。 引号中的 escape 字符也是可以
;;自动识别的。嵌套关系也是可以识别的。这一点可以和 VIM 中的 % 的功能类比。

(defun wcy-mark-some-thing-at-point()
  (interactive)
  (let* ((from (point))
         (a (mouse-start-end from from 1))
         (start (car a))
         (end (cadr a))
         (goto-point (if (= from start )
                         end
                       start)))
    (if (eq last-command 'wcy-mark-some-thing-at-point)
        (progn
          ;; exchange mark and point
          (goto-char (mark-marker))
          (set-marker (mark-marker) from))
      (push-mark (if (= goto-point start) end start) nil t)
      (when (and (interactive-p) (null transient-mark-mode))
        (goto-char (mark-marker))
        (sit-for 0 500 nil))
      (goto-char goto-point))))
(define-key global-map (kbd "s-m") 'wcy-mark-some-thing-at-point)
