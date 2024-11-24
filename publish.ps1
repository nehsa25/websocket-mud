
$build = (get-date).ToString("yyyyMMddHHmm");

write-host "Getting nehsamud ready...";
write-host "Building docker nehsamud image ${build}";
docker build . -t nehsa/nehsamud:$build --platform linux/amd64;

$cmd = "docker run -d --name nehsamud -p 60049:60049 -t nehsa/nehsamud:${build}";
 
write-host 'To run:';
write-host $cmd;

# output to file
$cmd | out-file -filepath ./run-api.ps1;
write-host 'To run in the future: ./run-api.ps1';

write-host "Done!";