-- This sample shows how to call a remote Web service whenever an
-- instance is received by Orthanc. For this sample to work, you have
-- to start the "CallWebService.js" script next to this file using
-- NodeJs.

-- Download and install the JSON module for Lua by Jeffrey Friedl
-- http://regex.info/blog/lua/json

-- NOTE : Replace "load" by "loadstring" for Lua <= 5.1
JSON = (load(HttpGet('http://regex.info/code/JSON.lua'))) ()

-- SetHttpCredentials('bachchu', 'admin@123')
-- SetHttpheader('Content-Type: application/json')
-- 'Content-Type: application/json',

function OnStoredInstance(instanceId, tags, metadata)
   -- Build the POST body

   local info = {}
   info['Patient_Sex'] = tags['PatientSex']
   info['Patient_Age'] = tags['PatientAge']
   info['Accession_Number'] = tags['AccessionNumber']
   info['Study_Time'] = tags['StudyTime'] 
   info['Patient_ID'] = tags['PatientID']
   info['Patient_Name'] = tags['PatientName']
   info['Study_Description'] = tags['StudyDescription']
   info['Study_Date'] = tags['StudyDate']
   info['Study_Instance_UID'] = tags['StudyInstanceUID']
   info['RemoteAET'] = ParseJson(RestApiGet('/instances/' .. instanceId .. '/metadata?expand'))["RemoteAET"]
   -- info['PatientName'] = tags['PatientName']
   -- info['PatientID'] = tags['PatientID']
   -- Send the POST request
   local headers = {
   ["content-type"] = "application/json",
}
   local answer = HttpPost('http://localhost:8000/core_app/api/v1/Studyinformation/', JSON:encode(info), headers)

   -- The answer equals "ERROR" in case of an error
   -- print('Web service called, answer received: ' .. answer)
   -- PrintRecursive(tags)
   -- PrintRecursive(tags)
   PrintRecursive(JSON:encode(info))
   -- patient = ParseJson(RestApiGet('/instances/' .. instanceId .. '/metadata?expand'))["RemoteAET"]
   -- PrintRecursive(patient)
   -- local study_uid = string.lower(patient)
   -- local re_study_uid = string.lower(tags['StudyInstanceUID'])
   -- PrintRecursive(study_uid)
   -- PrintRecursive(re_study_uid)
   -- if study_uid ~= re_study_uid then
   --    PrintRecursive(study_uid)
   --    PrintRecursive(re_study_uid)

   -- end

   -- PrintRecursive(patient)
   -- if (tags['StudyInstanceUID'] == patient['MainDicomTags']['StudyInstanceUID']) then
      -- PrintRecursive(patient['MainDicomTags']['StudyInstanceUID'])
end
