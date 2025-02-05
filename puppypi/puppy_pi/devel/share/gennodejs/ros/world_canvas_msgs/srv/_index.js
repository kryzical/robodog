
"use strict";

let GetAnnotations = require('./GetAnnotations.js')
let SetRelationship = require('./SetRelationship.js')
let SetKeyword = require('./SetKeyword.js')
let ListMaps = require('./ListMaps.js')
let DeleteMap = require('./DeleteMap.js')
let ListWorlds = require('./ListWorlds.js')
let EditAnnotationsData = require('./EditAnnotationsData.js')
let PubAnnotationsData = require('./PubAnnotationsData.js')
let SaveAnnotationsData = require('./SaveAnnotationsData.js')
let YAMLExport = require('./YAMLExport.js')
let RenameMap = require('./RenameMap.js')
let YAMLImport = require('./YAMLImport.js')
let PublishMap = require('./PublishMap.js')
let GetAnnotationsData = require('./GetAnnotationsData.js')
let DeleteAnnotations = require('./DeleteAnnotations.js')
let ResetDatabase = require('./ResetDatabase.js')
let SaveMap = require('./SaveMap.js')

module.exports = {
  GetAnnotations: GetAnnotations,
  SetRelationship: SetRelationship,
  SetKeyword: SetKeyword,
  ListMaps: ListMaps,
  DeleteMap: DeleteMap,
  ListWorlds: ListWorlds,
  EditAnnotationsData: EditAnnotationsData,
  PubAnnotationsData: PubAnnotationsData,
  SaveAnnotationsData: SaveAnnotationsData,
  YAMLExport: YAMLExport,
  RenameMap: RenameMap,
  YAMLImport: YAMLImport,
  PublishMap: PublishMap,
  GetAnnotationsData: GetAnnotationsData,
  DeleteAnnotations: DeleteAnnotations,
  ResetDatabase: ResetDatabase,
  SaveMap: SaveMap,
};
