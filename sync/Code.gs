// SHOW ME THE MONEY HQ - 기기 간 동기화용 구글 Apps Script
// 데이터는 내 구글 드라이브의 smtm-hq-data.json 파일 하나에 저장됩니다.
const FILE_NAME = 'smtm-hq-data.json';

function getFile_() {
  const it = DriveApp.getFilesByName(FILE_NAME);
  return it.hasNext() ? it.next() : null;
}
function out_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
function doGet(e) {
  try {
    const f = getFile_();
    return out_({ ok: true, data: f ? JSON.parse(f.getBlob().getDataAsString('UTF-8')) : null });
  } catch (err) { return out_({ ok: false, error: String(err) }); }
}
function doPost(e) {
  try {
    const body = JSON.parse(e.postData.contents);
    if (body.action !== 'save' || !body.data) return out_({ ok: false, error: '잘못된 요청' });
    const json = JSON.stringify(body.data);
    const f = getFile_();
    if (f) f.setContent(json); else DriveApp.createFile(FILE_NAME, json, 'application/json');
    return out_({ ok: true });
  } catch (err) { return out_({ ok: false, error: String(err) }); }
}
