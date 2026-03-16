from fastapi import FastAPI, File, Form, Response, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse
from geopy.distance import geodesic
import gpxpy
import io
import os
import shutil
from typing import Annotated
import zipfile

import download

AUTHOR_EMAIL = "anne.lhote@gmail.com"
AUTHOR_LINK = "https://github.com/annelhote"
AUTHOR_NAME = "Anne L'Hôte"

app = FastAPI()
app.include_router(download.router)

origins = ["http://localhost:3000"]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
  allow_headers=["Authorization", "Content-Type", "Accept"],
  max_age=3600,  # Cache preflight response for 1 hour (3600 seconds)
)


@app.get("/")
async def root():
  return { "message": "Hello World" }


@app.post("/split/")
async def split_gpx(gpx_file: Annotated[UploadFile, File()], gpx_id: Annotated[str, Form()], gpx_description: Annotated[str, Form()], distance_per_day: Annotated[int, Form()]) -> dict:
  contents = await gpx_file.read()
  gpx = gpxpy.parse(contents)
  total_distance = 0
  total_distance_e = 0
  dplus = 0
  dmoins = 0
  day = 0
  new_tracks = []
  if os.path.exists(gpx_id.lower()):
    shutil.rmtree(gpx_id.lower())
  os.makedirs(gpx_id.lower())
  for track in gpx.tracks:
    new_track = gpxpy.gpx.GPXTrack()
    new_tracks.append(new_track)
    for segment in track.segments:
      new_segment = gpxpy.gpx.GPXTrackSegment()
      new_track.segments.append(new_segment)
      for i in range(1, len(segment.points)):
        new_segment.points.append(gpxpy.gpx.GPXTrackPoint(segment.points[i - 1].latitude, segment.points[i - 1].longitude, elevation=segment.points[i - 1].elevation))
        point1 = segment.points[i - 1]
        point2 = segment.points[i]
        elevation_gain = point2.elevation - point1.elevation
        distance = geodesic((point1.latitude, point1.longitude), (point2.latitude, point2.longitude)).km
        total_distance += distance
        if elevation_gain > 0:
          total_distance_e += distance + (elevation_gain / 1000)
          dplus += abs(elevation_gain)
        else:
          total_distance_e += distance
          dmoins += abs(elevation_gain)
        if total_distance_e > (distance_per_day * (day + 1)):
          gpx_by_day = gpxpy.gpx.GPX()
          gpx_by_day.tracks = new_tracks
          gpx_by_day.description = gpx_description
          gpx_by_day.name = gpx_id
          gpx_by_day.author_email = AUTHOR_EMAIL
          gpx_by_day.author_link = AUTHOR_LINK
          gpx_by_day.author_name = AUTHOR_NAME
          with open(f"{gpx_id.lower()}/{gpx_id.lower()}_{day}.gpx", "w") as f:
            f.write(gpx_by_day.to_xml())
          day += 1
          new_tracks = []
          new_track = gpxpy.gpx.GPXTrack()
          new_tracks.append(new_track)
          new_segment = gpxpy.gpx.GPXTrackSegment()
          new_track.segments.append(new_segment)
  if os.path.exists("gr38.zip"):
    os.remove("gr38.zip")
  archive_path = shutil.make_archive(f"gr38", "zip", "gr38")
  return { "path": archive_path }
  # # return FileResponse(path=archive_path, filename="gr38.zip")
  # # zipped_file = io.BytesIO()
  # # with zipfile.ZipFile(zipped_file, "a", zipfile.ZIP_DEFLATED) as zipped:
  # #   # csv_data = StringIO()
  # #   # writer = csv.writer(csv_data, delimiter=',')
  # #   # writer.writerow(["test", "data"])
  # #   # csv_data.seek(0)
  # #   # csv_buffer = csv_data.read()
  # #   # buffer = 
  # #   stream = io.StringIO()
  # #   zipped.writestr(f"gr38_0.gpx", stream.write(open("gr38/gr38_0.gpx").read()))
  # #   zipped_file.seek(0)
  # # response = StreamingResponse(zipped_file, media_type="application/x-zip-compressed")
  # # response.headers["Content-Disposition"] = "attachment; filename=gr38.zip"
  # # return response
  # zip_filename = "gr38.zip"
  # s = io.BytesIO()
  # zf = zipfile.ZipFile(s, "w")
  # for fpath in [
  #   "gr38/gr38_0.gpx",
  #   "gr38/gr38_1.gpx",
  #   "gr38/gr38_2.gpx",
  #   "gr38/gr38_3.gpx",
  #   "gr38/gr38_4.gpx",
  #   "gr38/gr38_5.gpx",
  #   "gr38/gr38_6.gpx",
  #   "gr38/gr38_7.gpx",
  #   "gr38/gr38_8.gpx",
  #   "gr38/gr38_9.gpx",
  # ]:
  #     # Calculate path for file in zip
  #     fdir, fname = os.path.split(fpath)
  #     # Add file, at correct path
  #     zf.write(fpath, fname)
  # # Must close zip for all contents to be written
  # zf.close()
  # # Grab ZIP file from in-memory, make response with correct MIME-type
  # resp = Response(s.getvalue(), media_type="application/x-zip-compressed", headers={
  #     'Content-Disposition': f'attachment;filename={zip_filename}'
  # })
  # return resp

