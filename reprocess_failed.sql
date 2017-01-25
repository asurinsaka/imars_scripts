# this is to be put in the main ipopp server and run
# */30 * * * * date  >> /home/ipopp/reprocess_failed.log && /home/ipopp/drl/standalone/mariadb-10.1.8-linux-x86_64/bin/mysql -P 3666 -u dsm -pb28c935 DSM < /home/ipopp/reprocess_failed.sql >> /home/ipopp/reprocess_failed.log 2>&1

# no true color in night;
update Markers  left join Products as p on Markers.product=p.id set Markers.status = 1 where Markers.gopherColony in ('modis_tcolor_1km','modis_tcolor_250m') and Markers.status = 2  and hour(p.stopTime) <= 9 ;

#delete from Markers where status =2;
DELETE FROM Markers WHERE status = 2 AND product IN (SELECT id FROM Products WHERE creation >= DATE_SUB(CURDATE(), INTERVAL 1 DAY));
#DELETE FROM TransferCommands WHERE tableName='Products' AND tableId NOT IN (SELECT id FROM Products);

# Make sure that reprocess is full
#delete from Markers where gopherColony in ('project_sst_filtered','modis_sst_png')  and status = 2;
delete from Markers where gopherColony in ('Mod-L1a grp1') and status = 2;

# do not worry about failed mercator_sst, mercator_oc that is more than 1 day old
update Markers SET Markers.status = 1 where gopherColony in ('mercator_sst', 'mercator_oc') and status = 2 AND product IN (SELECT id FROM Products WHERE creation < DATE_SUB(CURDATE(), INTERVAL 1 DAY));
