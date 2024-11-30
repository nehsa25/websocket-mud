
$build = (get-date).ToString("yyyyMMddHHmm");
$localBuild = "./dist/nehsamud/browser";
$version = (get-date).ToString("yyyy-MM-dd HH:mm");
$full_version = "<!-- ${version} -->";
$index_location = "$localBuild/index.html";
$build_name = "nehsanet-mud-app";
$docker_name = "nehsa/nehsamud";

$val = 'both';
if ($val.ToLower() -eq '' -or $val.ToLower() -eq 'ui' -or $val.ToLower() -eq 'both') {
    if ($val.ToLower() -eq 'both') {
        write-host "Updating version.ts";
        set-content -path "./src/version.ts" -value "export const version = { number: '$version' }";
    }
    else {
        $val = read-host "Apply build number ${version}? [Y/n]";
        if ($val.ToLower() -eq '' -or $val.ToLower() -eq 'y') {
            write-host "Updating version.ts";
            set-content -path "./src/version.ts" -value "export const version = { number: '$version' }";
        }
    }
    
    write-host "Removing old files at $localBuild";
    remove-item -v $localBuild/* -recurse;
    
    write-host "Running: ng build --configuration production";
    ng build --configuration production;

    write-host "Updating wwwroot with Angular app";    
    if (Test-Path $localBuild) {
        if (Test-Path ../wwwroot) {
            write-host "Delete ../${build_name}/wwwroot for fresh contents";    
            remove-item -path ../wwwroot/* -force -recurse
        }
        write-host "Copying ${localBuild}: copy-item -force $localBuild/* ../wwwroot";
        copy-item -force -recurse -v $localBuild/* ../wwwroot
    }
   
    write-host "Updating index.html and version.ts with version info: ${version}";
    add-content -path $index_location -value $full_version;

    write-host "UI ready for deployment.";
}

write-host "Getting WEB ready...";
write-host "Building docker MUD image ${build}";
docker build . -t ${docker_name}:$build --platform linux/amd64;
    
write-host "Pushing MUD image to DockerHub...";
docker push ${docker_name}:$build;

$cmd = "docker run -p 80:80/tcp -p 443:443/tcp ${docker_name}:${build}";
write-host 'To run:';
write-host $cmd;

# output to file
$cmd | out-file -filepath ./run-api.ps1;
write-host 'To run in the future: ./run-api.ps1';

write-host "Done!";
