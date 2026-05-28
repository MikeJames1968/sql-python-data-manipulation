SELECT leg1.num, leg1.company, name, leg2.num, leg2.company
 FROM route leg1
 JOIN route tx1 ON leg1.num=tx1.num AND 
                   leg1.company=tx1.company
 JOIN route tx2 ON tx1.stop=tx2.stop
 JOIN route leg2 ON tx2.num=leg2.num AND
                    tx2.company=leg2.company
 JOIN stops ON (tx1.stop=id)
 WHERE leg1.stop=53
 AND   leg2.stop=147
 AND NOT (leg1.num=leg2.num AND
          leg1.company=leg2.company)
ORDER BY leg1.num, leg1.company, name, leg2.num,
         leg2.company
