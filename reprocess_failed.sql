-- delete Mod-L1A
-- DELETE FROM Markers WHERE status = 2 AND gopherColony IN ( 'Mod-L1A grp1', 'Mod-L1B grp1', 'modis_cloud_filter', 'modis_tcolor_1km', 'modis_tcolor_250m');
DELETE FROM Markers WHERE status = 2;

-- do not worry about mercator_sst or mercator_oc more than 1 day old
update Markers SET Markers.status = 1 where gopherColony in ('mercator_sst', 'mercator_oc') and status = 2 AND product IN (SELECT id FROM Products WHERE creation < DATE_SUB(CURDATE(), INTERVAL 1 DAY));

-- reporcess fails in 1 day
-- DELETE M FROM Markers AS M JOIN Products AS P ON M.product = P.id WHERE M.status = 2 AND P.creation > DATE_SUB(CURDATE(), INTERVAL 1 DAY);

-- ignore erros for product created 20 days ago
UPDATE  Markers AS M JOIN Products AS P ON M.product = P.id SET M.status = 1 WHERE M.status <> 1 AND P.creation < ADDDATE(NOW(), -20);

-- redo the mapping for the products from 6 hours ago
DELETE M FROM Markers AS M JOIN Products AS P ON M.product = P.id WHERE M.gopherColony IN ('project_sst_filtered', 'project_oc', 'modis_tcolor_250m') AND P.pass IN (select P1.id from Passes as P1 left join Passes as P2 on (P1.aos BETWEEN ADDTIME(P2.aos, "00:04:59") and ADDTIME(P2.aos,"00:30:01")) AND P1.spacecraft = P2.spacecraft WHERE (P1.aos BETWEEN ADDTIME(NOW(), "-07:00:00") AND ADDTIME(NOW(), "-06:00:00")) AND P2.id IS NULL);
