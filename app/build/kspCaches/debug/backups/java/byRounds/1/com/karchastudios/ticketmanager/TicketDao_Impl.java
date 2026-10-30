package com.karchastudios.ticketmanager;

import android.database.Cursor;
import androidx.annotation.NonNull;
import androidx.room.CoroutinesRoom;
import androidx.room.EntityDeletionOrUpdateAdapter;
import androidx.room.EntityInsertionAdapter;
import androidx.room.RoomDatabase;
import androidx.room.RoomSQLiteQuery;
import androidx.room.util.CursorUtil;
import androidx.room.util.DBUtil;
import androidx.sqlite.db.SupportSQLiteStatement;
import java.lang.Class;
import java.lang.Exception;
import java.lang.Long;
import java.lang.Object;
import java.lang.Override;
import java.lang.String;
import java.lang.SuppressWarnings;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.Callable;
import javax.annotation.processing.Generated;
import kotlin.Unit;
import kotlin.coroutines.Continuation;
import kotlinx.coroutines.flow.Flow;

@Generated("androidx.room.RoomProcessor")
@SuppressWarnings({"unchecked", "deprecation"})
public final class TicketDao_Impl implements TicketDao {
  private final RoomDatabase __db;

  private final EntityInsertionAdapter<Ticket> __insertionAdapterOfTicket;

  private final EntityDeletionOrUpdateAdapter<Ticket> __deletionAdapterOfTicket;

  private final EntityDeletionOrUpdateAdapter<Ticket> __updateAdapterOfTicket;

  public TicketDao_Impl(@NonNull final RoomDatabase __db) {
    this.__db = __db;
    this.__insertionAdapterOfTicket = new EntityInsertionAdapter<Ticket>(__db) {
      @Override
      @NonNull
      protected String createQuery() {
        return "INSERT OR ABORT INTO `tickets` (`id`,`firstName`,`lastName`,`venueType`,`ticketType`,`venue`,`location`,`date`,`time`,`seat`,`price`,`status`,`notes`,`code`) VALUES (nullif(?, 0),?,?,?,?,?,?,?,?,?,?,?,?,?)";
      }

      @Override
      protected void bind(@NonNull final SupportSQLiteStatement statement,
          @NonNull final Ticket entity) {
        statement.bindLong(1, entity.getId());
        statement.bindString(2, entity.getFirstName());
        statement.bindString(3, entity.getLastName());
        statement.bindString(4, entity.getVenueType());
        statement.bindString(5, entity.getTicketType());
        statement.bindString(6, entity.getVenue());
        statement.bindString(7, entity.getLocation());
        statement.bindString(8, entity.getDate());
        statement.bindString(9, entity.getTime());
        statement.bindString(10, entity.getSeat());
        statement.bindDouble(11, entity.getPrice());
        statement.bindString(12, entity.getStatus());
        statement.bindString(13, entity.getNotes());
        statement.bindString(14, entity.getCode());
      }
    };
    this.__deletionAdapterOfTicket = new EntityDeletionOrUpdateAdapter<Ticket>(__db) {
      @Override
      @NonNull
      protected String createQuery() {
        return "DELETE FROM `tickets` WHERE `id` = ?";
      }

      @Override
      protected void bind(@NonNull final SupportSQLiteStatement statement,
          @NonNull final Ticket entity) {
        statement.bindLong(1, entity.getId());
      }
    };
    this.__updateAdapterOfTicket = new EntityDeletionOrUpdateAdapter<Ticket>(__db) {
      @Override
      @NonNull
      protected String createQuery() {
        return "UPDATE OR ABORT `tickets` SET `id` = ?,`firstName` = ?,`lastName` = ?,`venueType` = ?,`ticketType` = ?,`venue` = ?,`location` = ?,`date` = ?,`time` = ?,`seat` = ?,`price` = ?,`status` = ?,`notes` = ?,`code` = ? WHERE `id` = ?";
      }

      @Override
      protected void bind(@NonNull final SupportSQLiteStatement statement,
          @NonNull final Ticket entity) {
        statement.bindLong(1, entity.getId());
        statement.bindString(2, entity.getFirstName());
        statement.bindString(3, entity.getLastName());
        statement.bindString(4, entity.getVenueType());
        statement.bindString(5, entity.getTicketType());
        statement.bindString(6, entity.getVenue());
        statement.bindString(7, entity.getLocation());
        statement.bindString(8, entity.getDate());
        statement.bindString(9, entity.getTime());
        statement.bindString(10, entity.getSeat());
        statement.bindDouble(11, entity.getPrice());
        statement.bindString(12, entity.getStatus());
        statement.bindString(13, entity.getNotes());
        statement.bindString(14, entity.getCode());
        statement.bindLong(15, entity.getId());
      }
    };
  }

  @Override
  public Object insert(final Ticket t, final Continuation<? super Long> $completion) {
    return CoroutinesRoom.execute(__db, true, new Callable<Long>() {
      @Override
      @NonNull
      public Long call() throws Exception {
        __db.beginTransaction();
        try {
          final Long _result = __insertionAdapterOfTicket.insertAndReturnId(t);
          __db.setTransactionSuccessful();
          return _result;
        } finally {
          __db.endTransaction();
        }
      }
    }, $completion);
  }

  @Override
  public Object delete(final Ticket t, final Continuation<? super Unit> $completion) {
    return CoroutinesRoom.execute(__db, true, new Callable<Unit>() {
      @Override
      @NonNull
      public Unit call() throws Exception {
        __db.beginTransaction();
        try {
          __deletionAdapterOfTicket.handle(t);
          __db.setTransactionSuccessful();
          return Unit.INSTANCE;
        } finally {
          __db.endTransaction();
        }
      }
    }, $completion);
  }

  @Override
  public Object update(final Ticket t, final Continuation<? super Unit> $completion) {
    return CoroutinesRoom.execute(__db, true, new Callable<Unit>() {
      @Override
      @NonNull
      public Unit call() throws Exception {
        __db.beginTransaction();
        try {
          __updateAdapterOfTicket.handle(t);
          __db.setTransactionSuccessful();
          return Unit.INSTANCE;
        } finally {
          __db.endTransaction();
        }
      }
    }, $completion);
  }

  @Override
  public Flow<List<Ticket>> all() {
    final String _sql = "SELECT * FROM tickets ORDER BY date, time";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 0);
    return CoroutinesRoom.createFlow(__db, false, new String[] {"tickets"}, new Callable<List<Ticket>>() {
      @Override
      @NonNull
      public List<Ticket> call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfId = CursorUtil.getColumnIndexOrThrow(_cursor, "id");
          final int _cursorIndexOfFirstName = CursorUtil.getColumnIndexOrThrow(_cursor, "firstName");
          final int _cursorIndexOfLastName = CursorUtil.getColumnIndexOrThrow(_cursor, "lastName");
          final int _cursorIndexOfVenueType = CursorUtil.getColumnIndexOrThrow(_cursor, "venueType");
          final int _cursorIndexOfTicketType = CursorUtil.getColumnIndexOrThrow(_cursor, "ticketType");
          final int _cursorIndexOfVenue = CursorUtil.getColumnIndexOrThrow(_cursor, "venue");
          final int _cursorIndexOfLocation = CursorUtil.getColumnIndexOrThrow(_cursor, "location");
          final int _cursorIndexOfDate = CursorUtil.getColumnIndexOrThrow(_cursor, "date");
          final int _cursorIndexOfTime = CursorUtil.getColumnIndexOrThrow(_cursor, "time");
          final int _cursorIndexOfSeat = CursorUtil.getColumnIndexOrThrow(_cursor, "seat");
          final int _cursorIndexOfPrice = CursorUtil.getColumnIndexOrThrow(_cursor, "price");
          final int _cursorIndexOfStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "status");
          final int _cursorIndexOfNotes = CursorUtil.getColumnIndexOrThrow(_cursor, "notes");
          final int _cursorIndexOfCode = CursorUtil.getColumnIndexOrThrow(_cursor, "code");
          final List<Ticket> _result = new ArrayList<Ticket>(_cursor.getCount());
          while (_cursor.moveToNext()) {
            final Ticket _item;
            final long _tmpId;
            _tmpId = _cursor.getLong(_cursorIndexOfId);
            final String _tmpFirstName;
            _tmpFirstName = _cursor.getString(_cursorIndexOfFirstName);
            final String _tmpLastName;
            _tmpLastName = _cursor.getString(_cursorIndexOfLastName);
            final String _tmpVenueType;
            _tmpVenueType = _cursor.getString(_cursorIndexOfVenueType);
            final String _tmpTicketType;
            _tmpTicketType = _cursor.getString(_cursorIndexOfTicketType);
            final String _tmpVenue;
            _tmpVenue = _cursor.getString(_cursorIndexOfVenue);
            final String _tmpLocation;
            _tmpLocation = _cursor.getString(_cursorIndexOfLocation);
            final String _tmpDate;
            _tmpDate = _cursor.getString(_cursorIndexOfDate);
            final String _tmpTime;
            _tmpTime = _cursor.getString(_cursorIndexOfTime);
            final String _tmpSeat;
            _tmpSeat = _cursor.getString(_cursorIndexOfSeat);
            final double _tmpPrice;
            _tmpPrice = _cursor.getDouble(_cursorIndexOfPrice);
            final String _tmpStatus;
            _tmpStatus = _cursor.getString(_cursorIndexOfStatus);
            final String _tmpNotes;
            _tmpNotes = _cursor.getString(_cursorIndexOfNotes);
            final String _tmpCode;
            _tmpCode = _cursor.getString(_cursorIndexOfCode);
            _item = new Ticket(_tmpId,_tmpFirstName,_tmpLastName,_tmpVenueType,_tmpTicketType,_tmpVenue,_tmpLocation,_tmpDate,_tmpTime,_tmpSeat,_tmpPrice,_tmpStatus,_tmpNotes,_tmpCode);
            _result.add(_item);
          }
          return _result;
        } finally {
          _cursor.close();
        }
      }

      @Override
      protected void finalize() {
        _statement.release();
      }
    });
  }

  @NonNull
  public static List<Class<?>> getRequiredConverters() {
    return Collections.emptyList();
  }
}
