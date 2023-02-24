<?php
$inputCharacters = ['-','/','?','@','!','*','#','%','&','{','}','<','>',' ','$','!',':','+','`','|','=','123','\\','\''];
$filenameFirst  = "new";
$filenameSecond  = "file";
$outputFilename =[];

foreach ($inputCharacters as $inputCharacter) {
   $addMiddleCharacter = $filenameFirst.$inputCharacter.$filenameSecond;
   $addStartCharacter = $inputCharacter.$filenameFirst.$filenameSecond;
   $addMiEndCharacter = $filenameFirst.$filenameSecond.$inputCharacter;
   array_push($outputFilename,$addMiddleCharacter, $addStartCharacter, $addMiEndCharacter);
}
print_r($outputFilename);
