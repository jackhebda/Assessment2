from __future__ import absolute_import
from app.db.db import DB
from app.models.base import Base
from app.models.zipcode import ZipCodeRiskFactor
from fastapi import HTTPException
from redis import Redis

r = Redis(host='redis', port=6379, decode_responses=True)

class ZipCodeRepository(Base):
    db: DB

    async def get(self, zipcode: int) -> ZipCodeRiskFactor:
 
        if r.exists(zipcode):
            return {"zipcode": zipcode,
                "risk_factor": r.get(zipcode).decode()}

        query = "SELECT * FROM riskfactor WHERE zipcode = :zipcode"
        results = await self.db.conn.fetch_one(query = query, values={"zipcode": zipcode})
        
        if not results:
            raise HTTPException(status_code=400, detail="Zipcode not in the dataset")
        
        r.set(zipcode, results[1])

        return {
            "zipcode":zipcode,
            "risk_factor":results[1]}
