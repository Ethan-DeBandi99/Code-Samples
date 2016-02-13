(define operators (list (operator 'new :action '(takeOff $x $y)
				:precond '((clear $x) (on $x $y))
				:effect-add '((onTable $x) (clear $y))
				:effect-delete '((on $x $y)) )
			(operator 'new :action '(putOn $x $y)
				:precond '((clear $x) (onTable $x) (clear $y))
				:effect-add '((on $x $y))
				:effect-delete '((onTable $x) (clear $y)) )
		  )
)

(define init '((onTable B) (onTable A) (on C A) (clear B) (clear C)))

(define goal '((onTable C) (on B C) (on A B) (clear A)))
