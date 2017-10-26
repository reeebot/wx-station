<?php

$command = escapeshellcmd('sudo python readtheData.py');
$output = shell_exec($command);
echo $output;



?>