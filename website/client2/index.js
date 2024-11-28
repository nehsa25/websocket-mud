import express from 'express';
const app = express();
app.use(express.json());
app.use(express.static('dist/nehsanet/browser'))
const port = process.env.PORT || 80;

app.listen(port, () => {
    console.log(`Listening on port ${port}`);
});
