<?php 
$data['status'] = "num";
$infos = [];
$item = array("CarId"=>"123",
		"ArriveTime"=>"123",
		"ParkPlace"=>"123",
		"Fee"=>"123",
		"BackPersons"=>"123",
		"BoxNum"=>"123");

for($i = 0 ; $i < 10 ; $i++){
	array_push($infos,$item);
}
$data['infos'] = $infos;
echo json_encode($data);
