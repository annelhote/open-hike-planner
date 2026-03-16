import { Box, Breadcrumbs, Button, FormControl, FormHelperText, Input, InputLabel, Link, Stack, TextareaAutosize, Typography } from "@mui/material";
import axios from "axios";
import { useState } from "react";

const Tools = () => {
  const [gpxFile, setGpxFile] = useState(null);
  const [gpxId, setGpxId] = useState("");
  const [gpxDescrption, setGpxDescription] = useState("");
  // const [phnNumber, setPhoneNumber] = useState("");
  // const [dateOfBirth, setDateOfBirth] = useState("");
  // const [password, setPassword] = useState("");
  // const [cnfpassword, setcnfPassword] = useState("");
  // const [checked, setChecked] = useState(false);
  // const [checkedUpdates, setCheckedUpdates] = useState(true);
  const [status, setStatus] = useState("");

  const handleSubmit = async (event) => {
    setStatus("");
    event.preventDefault();
    const formData = new FormData();
    formData.append("gpx_file", gpxFile);
    formData.append("gpx_id", gpxId);
    formData.append("gpx_description", gpxDescrption);
    formData.append("distance_per_day", "25");
    try {
      const resp = await axios.post("http://localhost:8000/split/", formData, {
        headers: { "content-type": "multipart/form-data" },
      });
      console.log(resp.status);
      console.log(resp.data);
      setStatus(resp.status === 200 ? "Thank you!" : "Error.");
      // Step 4: Create object URL and trigger download
      // const blob = new Blob([new Uint8Array(resp.data)]);
      const blob = new Blob([resp.data], {type: "application/x-zip-compressed"});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = "gr38.zip";
      document.body.appendChild(a); // Required for Firefox
      a.click();
      // Step 5: Clean up
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error(error)
      setStatus("Error");
    }
  }

  return (
    <Box className="open-trail blog" sx={{ flexGrow: 0.75 }}>
      <Breadcrumbs aria-label="breadcrumb" color="color.secondary">
        <Link color="inherit" href="#" underline="hover">
          Open Trail
        </Link>
        <Typography>Tools</Typography>
      </Breadcrumbs>
      <form style={{ paddingTop: "10px", paddingLeft: "500px" }} onSubmit={handleSubmit}>
        <Stack spacing={2} direction="row" sx={{ marginBottom: 4 }}>
          <FormControl>
            <InputLabel htmlFor="gpxFile">GPX</InputLabel>
            <Input
              autoFocus={true}
              type="file"
              id="gpxFile"
              value={gpxFile?.filename}
              onChange={(e) => { console.log(e.target); setGpxFile(e.target.files[0]);}}
              // slotProps={{ input: { inputprops: { accept: "application/gpx, application/gpx+xml" } } }}
              // inputProps={{accept:"application/gpx, application/gpx+xml"}}
              // slotProps={{ input: { InputProps: { accept: "application/gpx" } } }}
              inputProps={{
                multiple: true,
                accept: "application/xml"
              }}
            />
            <FormHelperText id="my-helper-text">
              Charger ici votre fichier GPX
            </FormHelperText>
          </FormControl>
          <FormControl>
            <InputLabel htmlFor="gpxId">Identifiant</InputLabel>
            <Input
              id="gpxId"
              onChange={(e) => setGpxId(e.target.value)}
              value={gpxId}
            />
            <FormHelperText id="my-helper-text">
              Saisir l'identifiant de votre trajet
            </FormHelperText>
          </FormControl>
        </Stack>
        <Stack spacing={2} direction="row" sx={{ marginBottom: 4 }}>
          <FormControl>
            <InputLabel htmlFor="gpxDescrption">Description</InputLabel>
            <TextareaAutosize
              aria-describedby="my-helper-text"
              id="gpxDescrption"
              maxRows={4}
              onChange={(e) => setGpxDescription(e.target.value)}
              value={gpxDescrption}
            />
            <FormHelperText id="my-helper-text">
              Description du trajet
            </FormHelperText>
          </FormControl>
        </Stack>
        <Button variant="contained" color="success" type="submit">
          Envoyer
        </Button>
      </form>
      {status ? <h1>{status}</h1> : null}
    </Box>
  );
};

export default Tools;